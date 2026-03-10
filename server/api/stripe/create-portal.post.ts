import { serverSupabaseUser } from '#supabase/server'
import { useStripe } from '../../utils/stripe'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const supabase = useServerSupabase()
  const stripe = useStripe()
  const config = useRuntimeConfig()

  const { data: profile } = await supabase
    .from('profiles')
    .select('stripe_customer_id')
    .eq('id', user.id)
    .single()

  const customerId = profile?.stripe_customer_id as string | null

  if (!customerId) {
    throw createError({ statusCode: 404, message: 'Aucun abonnement trouvé' })
  }

  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: `${config.public.appUrl}/settings/billing`
  })

  return { url: session.url }
})
