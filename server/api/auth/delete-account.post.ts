import { serverSupabaseUser } from '#supabase/server'
import { createClient } from '@supabase/supabase-js'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const supabase = useServerSupabase()

  // Cancel Stripe subscription if any
  try {
    const { data: profile } = await supabase
      .from('profiles')
      .select('stripe_subscription_id, stripe_customer_id')
      .eq('id', user.id)
      .single()

    if (profile?.stripe_subscription_id) {
      const { useStripe } = await import('../../utils/stripe')
      const stripe = useStripe()
      await stripe.subscriptions.cancel(profile.stripe_subscription_id as string)
    }
  }
  catch (err) {
    console.error('Stripe cancellation failed (non-blocking):', err)
  }

  // Delete CV files from Storage
  const { data: cvFiles } = await supabase
    .from('cvs')
    .select('file_path')
    .eq('user_id', user.id)

  if (cvFiles && cvFiles.length > 0) {
    const paths = cvFiles.map(cv => cv.file_path as string)
    await supabase.storage.from('cvs').remove(paths)
  }

  // Delete user from auth (cascades to profiles, cvs, analyses via FK)
  const adminClient = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!,
    { auth: { persistSession: false } }
  )

  const { error } = await adminClient.auth.admin.deleteUser(user.id)

  if (error) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la suppression du compte' })
  }

  return { success: true }
})
