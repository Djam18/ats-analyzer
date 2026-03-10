import { serverSupabaseUser } from '#supabase/server'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const id = getRouterParam(event, 'id')
  if (!id || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
    throw createError({ statusCode: 400, message: 'ID invalide' })
  }

  const supabase = useServerSupabase()

  // Verify ownership and get file path
  const { data: cv, error: fetchError } = await supabase
    .from('cvs')
    .select('id, file_path')
    .eq('id', id)
    .eq('user_id', user.id)
    .single()

  if (fetchError || !cv) {
    throw createError({ statusCode: 404, message: 'CV introuvable' })
  }

  // Delete from Storage
  const { error: storageError } = await supabase.storage
    .from('cvs')
    .remove([cv.file_path])

  if (storageError) {
    console.error('Storage delete error:', storageError)
    // Continue — DB record should still be deleted
  }

  // Delete from DB (analyses are kept, orphan reference is acceptable)
  const { error: dbError } = await supabase
    .from('cvs')
    .delete()
    .eq('id', id)
    .eq('user_id', user.id)

  if (dbError) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la suppression' })
  }

  return { success: true }
})
