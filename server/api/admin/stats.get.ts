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

  const supabase = useServerSupabase()

  // Single query for both referral + plan breakdown
  const { data: profileRows } = await supabase
    .from('profiles')
    .select('plan, referral_source')

  const referralCounts: Record<string, number> = {}
  const planCounts: Record<string, number> = {}

  for (const row of profileRows ?? []) {
    const source = (row as any).referral_source ?? 'unknown'
    const plan = (row as any).plan ?? 'free'
    referralCounts[source] = (referralCounts[source] ?? 0) + 1
    planCounts[plan] = (planCounts[plan] ?? 0) + 1
  }

  const totalUsers = (profileRows ?? []).length

  // Total analyses
  const { count: totalAnalyses } = await supabase
    .from('analyses')
    .select('id', { count: 'exact', head: true })
    .eq('status', 'completed')

  // New users last 7 days
  const sevenDaysAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
  const { count: newUsersWeek } = await supabase
    .from('profiles')
    .select('id', { count: 'exact', head: true })
    .gte('created_at', sevenDaysAgo)

  // New users last 30 days
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString()
  const { count: newUsersMonth } = await supabase
    .from('profiles')
    .select('id', { count: 'exact', head: true })
    .gte('created_at', thirtyDaysAgo)

  // Conversion rate free -> paid
  const paidUsers = (planCounts.pro ?? 0) + (planCounts.expert ?? 0)
  const conversionRate = totalUsers > 0 ? Math.round((paidUsers / totalUsers) * 100) : 0

  return {
    totalUsers,
    totalAnalyses: totalAnalyses ?? 0,
    newUsersWeek: newUsersWeek ?? 0,
    newUsersMonth: newUsersMonth ?? 0,
    paidUsers,
    conversionRate,
    planCounts,
    referralCounts
  }
})
