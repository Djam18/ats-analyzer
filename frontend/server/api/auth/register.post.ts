// ============================================================
// POST /api/auth/register
//
// Solves the chicken-and-egg RLS problem:
//   1. Creates the Supabase auth user (service role — bypasses RLS)
//   2. Creates the ats.organizations row
//   3. Creates the ats.user_orgs row (admin role)
//   4. Creates the default ats.pipeline_stages for the org
//
// The client receives the Supabase session token and logs in
// via the normal anon client (useAuth().signIn) after this call.
// ============================================================


interface RegisterBody {
  email: string
  password: string
  firstName: string
  lastName: string
  company: string
}

const DEFAULT_STAGES = [
  { name: 'Candidatures reçues', color: '#718096', position: 1, is_default: true },
  { name: 'Présélection', color: '#3182CE', position: 2, is_default: false },
  { name: 'Entretien RH', color: '#805AD5', position: 3, is_default: false },
  { name: 'Entretien technique', color: '#D69E2E', position: 4, is_default: false },
  { name: 'Offre envoyée', color: '#38A169', position: 5, is_default: false },
  { name: 'Refusé', color: '#E53E3E', position: 6, is_default: false },
]

function slugify(str: string): string {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60)
}

export default defineEventHandler(async (event) => {
  const body = await readBody<RegisterBody>(event)

  const { email, password, firstName, lastName, company } = body

  if (!email || !password || !firstName || !lastName) {
    throw createError({ statusCode: 400, message: 'Missing required fields' })
  }

  const supabase = useSupabaseAdmin()

  // 1. Create auth user
  const { data: authData, error: authError } = await supabase.auth.admin.createUser({
    email,
    password,
    email_confirm: false,
    user_metadata: {
      first_name: firstName,
      last_name: lastName,
    },
  })

  if (authError) {
    const message = authError.message.includes('already registered')
      ? 'Cette adresse email est déjà utilisée.'
      : authError.message
    throw createError({ statusCode: 422, message })
  }

  const userId = authData.user.id

  // 2-4. Create org + user_org + pipeline stages via a single RPC call
  // (bypasses PostgREST schema restriction — runs as SECURITY DEFINER in public schema)
  const orgName = company?.trim() || `${firstName} ${lastName}`
  const baseSlug = slugify(orgName) || slugify(email.split('@')[0])
  const slug = `${baseSlug}-${userId.slice(0, 8)}`

  const { data: orgId, error: rpcError } = await supabase.rpc('register_user_org', {
    p_user_id: userId,
    p_org_name: orgName,
    p_slug: slug,
  })

  if (rpcError) {
    await supabase.auth.admin.deleteUser(userId)
    throw createError({ statusCode: 500, message: 'Failed to create organization' })
  }

  return { success: true, userId, orgId }
})
