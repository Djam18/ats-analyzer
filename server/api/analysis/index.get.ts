import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const query = getQuery(event)
  const page = Math.max(1, Number(query.page) || 1)
  const limit = 20
  const offset = (page - 1) * limit

  const supabase = useServerSupabase()

  const { data, error, count } = await supabase
    .from('analyses')
    .select('id, status, score, job_title, company_name, created_at, cvs(display_name)', { count: 'exact' })
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })
    .range(offset, offset + limit - 1)

  if (error) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la récupération des analyses' })
  }

  return {
    data,
    meta: { total: count ?? 0, page, limit, pages: Math.ceil((count ?? 0) / limit) }
  }
})
