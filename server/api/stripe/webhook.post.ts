import Stripe from 'stripe'
import { useStripe } from '../../utils/stripe'

// Disable body parsing — Stripe requires raw body for signature verification
export const config = { bodyParser: false }

function getPlanFromPriceId(priceId: string): string {
  const runtimeConfig = useRuntimeConfig()
  if (priceId === runtimeConfig.public.stripePriceProMonthly) return 'pro'
  if (priceId === runtimeConfig.public.stripePriceExpertMonthly) return 'expert'
  return 'free'
}

async function updateProfileSubscription(
  supabase: ReturnType<typeof useServerSupabase>,
  profileId: string,
  subscription: Stripe.Subscription,
  getPlan: (priceId: string) => string
) {
  const priceId = subscription.items.data[0]?.price.id ?? ''
  await supabase
    .from('profiles')
    .update({
      plan: getPlan(priceId),
      stripe_subscription_id: subscription.id,
      subscription_status: subscription.status
    })
    .eq('id', profileId)
}

export default defineEventHandler(async (event) => {
  const stripe = useStripe()
  const config = useRuntimeConfig()
  const supabase = useServerSupabase()

  // Read raw body for signature verification
  const rawBody = await readRawBody(event)
  const signature = getHeader(event, 'stripe-signature')

  if (!rawBody || !signature) {
    throw createError({ statusCode: 400, message: 'Missing body or signature' })
  }

  let stripeEvent: Stripe.Event
  try {
    stripeEvent = stripe.webhooks.constructEvent(rawBody, signature, config.stripeWebhookSecret)
  }
  catch (err: unknown) {
    console.error('Stripe webhook signature verification failed:', err)
    throw createError({ statusCode: 400, message: 'Invalid signature' })
  }

  // Idempotency check
  const { data: existing } = await supabase
    .from('webhook_events')
    .select('id')
    .eq('stripe_event_id', stripeEvent.id)
    .single()

  if (existing) {
    return { received: true, skipped: true }
  }

  // Log event for idempotency
  await supabase
    .from('webhook_events')
    .insert({ stripe_event_id: stripeEvent.id, event_type: stripeEvent.type })

  // Handle events
  switch (stripeEvent.type) {
    case 'checkout.session.completed': {
      const session = stripeEvent.data.object as Stripe.Checkout.Session
      const userId = session.metadata?.supabase_user_id

      if (!userId || !session.subscription) {
        console.error('checkout.session.completed missing metadata or subscription', { eventId: stripeEvent.id })
        break
      }

      const subscription = await stripe.subscriptions.retrieve(session.subscription as string)
      await updateProfileSubscription(supabase, userId, subscription, getPlanFromPriceId)
      break
    }

    case 'customer.subscription.updated': {
      const subscription = stripeEvent.data.object as Stripe.Subscription
      const userId = subscription.metadata?.supabase_user_id

      if (!userId) {
        // Fall back to lookup by stripe_customer_id
        const { data: profile } = await supabase
          .from('profiles')
          .select('id')
          .eq('stripe_customer_id', subscription.customer as string)
          .single()

        if (!profile) break
        await updateProfileSubscription(supabase, profile.id, subscription, getPlanFromPriceId)
        break
      }

      await updateProfileSubscription(supabase, userId, subscription, getPlanFromPriceId)
      break
    }

    case 'customer.subscription.deleted': {
      const subscription = stripeEvent.data.object as Stripe.Subscription

      const { data: profile } = await supabase
        .from('profiles')
        .select('id')
        .eq('stripe_customer_id', subscription.customer as string)
        .single()

      if (!profile) break

      await supabase
        .from('profiles')
        .update({
          plan: 'free',
          stripe_subscription_id: null,
          subscription_status: 'canceled'
        })
        .eq('id', profile.id)
      break
    }

    case 'invoice.payment_failed': {
      const invoice = stripeEvent.data.object as Stripe.Invoice

      const { data: profile } = await supabase
        .from('profiles')
        .select('id')
        .eq('stripe_customer_id', invoice.customer as string)
        .single()

      if (!profile) break

      await supabase
        .from('profiles')
        .update({ subscription_status: 'past_due' })
        .eq('id', profile.id)
      break
    }

    default:
      break
  }

  return { received: true }
})
