import Stripe from 'stripe'

let stripeClient: Stripe | null = null

export function useStripe(): Stripe {
  if (stripeClient) return stripeClient

  const key = process.env.STRIPE_SECRET_KEY
  if (!key) throw new Error('STRIPE_SECRET_KEY is required')

  stripeClient = new Stripe(key, { apiVersion: '2025-02-24.acacia' })
  return stripeClient
}

export function getPriceId(plan: 'pro' | 'expert'): string {
  return plan === 'pro'
    ? process.env.NUXT_PUBLIC_STRIPE_PRICE_PRO_MONTHLY ?? ''
    : process.env.NUXT_PUBLIC_STRIPE_PRICE_EXPERT_MONTHLY ?? ''
}
