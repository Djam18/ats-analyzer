import { serverSupabaseUser } from '#supabase/server'
import { checkQuota } from '../../utils/quota'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const supabase = useServerSupabase()
  const quota = await checkQuota(supabase, user.id)

  // Also fetch subscription_status for billing page display
  const { data: profile } = await supabase
    .from('profiles')
    .select('subscription_status')
    .eq('id', user.id)
    .single()

  return {
    ...quota,
    subscription_status: (profile as any)?.subscription_status ?? null
  }
})
