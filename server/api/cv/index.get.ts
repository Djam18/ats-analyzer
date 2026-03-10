import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const supabase = useServerSupabase()

  const { data, error } = await supabase
    .from('cvs')
    .select('id, display_name, file_name, file_type, file_size, is_scanned, page_count, created_at')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })

  if (error) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la récupération des CV' })
  }

  return data
})
