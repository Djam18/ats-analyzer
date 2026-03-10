import { defineEventHandler, getRequestIP, createError } from 'h3'

// Simple in-memory rate limiter (resets on server restart)
// For production, replace with Redis-backed solution

interface RateLimitEntry {
  count: number
  resetAt: number
}

const store = new Map<string, RateLimitEntry>()

const LIMITS: Record<string, { max: number, windowMs: number }> = {
  '/api/analysis/create': { max: 10, windowMs: 60 * 60 * 1000 },   // 10/hour
  '/api/cv/upload': { max: 20, windowMs: 60 * 60 * 1000 },          // 20/hour
  '/api/auth/send-welcome': { max: 3, windowMs: 60 * 60 * 1000 },   // 3/hour
  '/api/stripe/create-checkout': { max: 10, windowMs: 60 * 60 * 1000 } // 10/hour
}

function checkRateLimit(key: string, max: number, windowMs: number): boolean {
  const now = Date.now()
  const entry = store.get(key)

  if (!entry || now > entry.resetAt) {
    store.set(key, { count: 1, resetAt: now + windowMs })
    return true
  }

  if (entry.count >= max) return false

  entry.count++
  return true
}

export default defineEventHandler((event) => {
  const path = event.path
  const limit = LIMITS[path]
  if (!limit) return

  const ip = getRequestIP(event, { xForwardedFor: true }) ?? 'unknown'
  const key = `${path}:${ip}`

  if (!checkRateLimit(key, limit.max, limit.windowMs)) {
    throw createError({
      statusCode: 429,
      message: 'Trop de requêtes. Veuillez réessayer plus tard.'
    })
  }
})
