import { serverSupabaseUser } from '#supabase/server'
import { z } from 'zod'
import { useStripe, getPriceId } from '../../utils/stripe'

const schema = z.object({
  plan: z.enum(['pro', 'expert'])
})

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const body = await readBody(event)
  const parsed = schema.safeParse(body)
  if (!parsed.success) {
    throw createError({ statusCode: 422, message: 'Plan invalide' })
  }

  const { plan } = parsed.data
  const supabase = useServerSupabase()
  const stripe = useStripe()
  const config = useRuntimeConfig()

  // Get or create Stripe customer
  const { data: profile } = await supabase
    .from('profiles')
    .select('stripe_customer_id, full_name')
    .eq('id', user.id)
    .single()

  let customerId = profile?.stripe_customer_id as string | null

  if (!customerId) {
    const customer = await stripe.customers.create({
      email: user.email,
      name: (profile?.full_name as string) ?? undefined,
      metadata: { supabase_user_id: user.id }
    })
    customerId = customer.id

    await supabase
      .from('profiles')
      .update({ stripe_customer_id: customerId })
      .eq('id', user.id)
  }

  const priceId = getPriceId(plan)
  const appUrl = config.public.appUrl

  const session = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${appUrl}/dashboard?upgraded=1`,
    cancel_url: `${appUrl}/pricing`,
    subscription_data: {
      metadata: { supabase_user_id: user.id, plan }
    },
    allow_promotion_codes: true
  })

  if (!session.url) {
    throw createError({ statusCode: 500, message: 'Impossible de créer la session de paiement' })
  }

  return { url: session.url }
})
