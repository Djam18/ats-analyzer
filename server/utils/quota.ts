import type { SupabaseClient } from '@supabase/supabase-js'

const FREE_LIMIT = 3
const PRO_MONTHLY_LIMIT = 50

export interface QuotaResult {
  allowed: boolean
  remaining: number
  plan: string
  used: number
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function checkQuota(supabase: SupabaseClient<any, 'public', any>, userId: string): Promise<QuotaResult> {
  const { data: profile, error } = await supabase
    .from('profiles')
    .select('plan, free_analyses_used, subscription_status')
    .eq('id', userId)
    .single()

  if (error || !profile) {
    throw new Error('Profil utilisateur introuvable')
  }

  const plan = profile.plan as string

  if (plan === 'expert') {
    return { allowed: true, remaining: Infinity, plan, used: 0 }
  }

  if (plan === 'pro') {
    // Check subscription is still active
    if (profile.subscription_status !== 'active') {
      return { allowed: false, remaining: 0, plan, used: 0 }
    }

    // Count completed analyses this calendar month
    const startOfMonth = new Date()
    startOfMonth.setDate(1)
    startOfMonth.setHours(0, 0, 0, 0)

    const { count, error: countError } = await supabase
      .from('analyses')
      .select('id', { count: 'exact', head: true })
      .eq('user_id', userId)
      .eq('status', 'completed')
      .gte('created_at', startOfMonth.toISOString())

    if (countError) throw new Error('Erreur lors du calcul du quota')

    const used = count ?? 0
    const remaining = Math.max(0, PRO_MONTHLY_LIMIT - used)
    return { allowed: remaining > 0, remaining, plan, used }
  }

  // Free plan
  const used = profile.free_analyses_used as number
  const remaining = Math.max(0, FREE_LIMIT - used)
  return { allowed: remaining > 0, remaining, plan, used }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function consumeQuota(supabase: SupabaseClient<any, 'public', any>, userId: string, plan: string): Promise<void> {
  if (plan === 'free') {
    const { error } = await supabase.rpc('increment_free_analyses', { p_user_id: userId })
    if (error) throw new Error('Erreur lors de la mise à jour du quota')
  }
  // Pro/Expert: quota tracked by counting completed analyses — no explicit increment needed
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function refundQuota(supabase: SupabaseClient<any, 'public', any>, userId: string, plan: string): Promise<void> {
  if (plan === 'free') {
    // Decrement free_analyses_used but never below 0
    await supabase.rpc('decrement_free_analyses', { p_user_id: userId })
  }
  // Pro/Expert: quota is based on completed analysis count, so a failed (non-completed) analysis auto-refunds
}
