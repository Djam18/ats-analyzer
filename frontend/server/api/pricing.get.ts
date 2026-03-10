import Stripe from 'stripe'

export default defineEventHandler(async () => {
  const secretKey = process.env.STRIPE_SECRET_KEY
  if (!secretKey) {
    throw createError({ statusCode: 500, message: 'STRIPE_SECRET_KEY not configured' })
  }

  const stripe = new Stripe(secretKey)

  const priceIds = [
    process.env.STRIPE_PRICE_BASIC,
    process.env.STRIPE_PRICE_PRO,
  ].filter(Boolean) as string[]

  const prices = await Promise.all(
    priceIds.map((id) =>
      stripe.prices.retrieve(id, { expand: ['product'] })
    )
  )

  return prices.map((price) => {
    const product = price.product as Stripe.Product
    return {
      id: price.id,
      name: product.name,
      description: product.description ?? null,
      amount: price.unit_amount ? price.unit_amount / 100 : 0,
      currency: price.currency.toUpperCase(),
      interval: price.recurring?.interval ?? null,
      metadata: product.metadata ?? {},
    }
  })
})
