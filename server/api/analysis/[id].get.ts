import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const id = getRouterParam(event, 'id')
  if (!id || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
    throw createError({ statusCode: 400, message: 'ID manquant' })
  }

  const supabase = useServerSupabase()

  const { data, error } = await supabase
    .from('analyses')
    .select(`
      id, status, score, job_title, company_name, created_at, completed_at,
      matched_keywords, missing_keywords, analysis_details, error_message,
      cvs (id, display_name, file_type)
    `)
    .eq('id', id)
    .eq('user_id', user.id)
    .single()

  if (error || !data) {
    throw createError({ statusCode: 404, message: 'Analyse introuvable' })
  }

  return data
})
