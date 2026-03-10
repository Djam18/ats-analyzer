import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const config = useRuntimeConfig()
  const adminEmail = config.adminEmail as string | undefined

  if (!adminEmail || user.email?.toLowerCase() !== adminEmail.toLowerCase()) {
    throw createError({ statusCode: 403, message: 'Accès refusé' })
  }

  return { ok: true }
})
