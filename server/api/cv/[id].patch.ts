import { serverSupabaseUser } from '#supabase/server'
import { z } from 'zod'

const schema = z.object({
  display_name: z.string().min(1).max(100)
})

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const id = getRouterParam(event, 'id')
  if (!id || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
    throw createError({ statusCode: 400, message: 'ID invalide' })
  }

  const body = await readBody(event)
  const parsed = schema.safeParse(body)
  if (!parsed.success) {
    throw createError({ statusCode: 422, message: parsed.error.errors[0]?.message ?? 'Données invalides' })
  }

  const supabase = useServerSupabase()

  const { data, error } = await supabase
    .from('cvs')
    .update({ display_name: parsed.data.display_name })
    .eq('id', id)
    .eq('user_id', user.id)
    .select('id, display_name')
    .single()

  if (error) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la mise à jour' })
  }

  return data
})
