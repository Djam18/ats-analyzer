import { defineEventHandler, getRequestIP, createError } from 'h3'
import Redis from 'ioredis'

const LIMITS: Record<string, { max: number, windowSec: number }> = {
  '/api/analysis/create': { max: 10, windowSec: 3600 },
  '/api/cv/upload': { max: 20, windowSec: 3600 },
  '/api/auth/send-welcome': { max: 3, windowSec: 3600 },
  '/api/stripe/create-checkout': { max: 10, windowSec: 3600 }
}

// Redis-backed rate limiter (uses INCR + EXPIRE — atomic)
let redis: Redis | null = null

function getRedis(): Redis | null {
  if (redis) return redis
  const url = process.env.REDIS_URL
  if (!url) return null
  redis = new Redis(url, { lazyConnect: true, enableOfflineQueue: false })
  redis.on('error', () => { redis = null }) // fall back to in-memory on failure
  return redis
}

// In-memory fallback
interface Entry { count: number, resetAt: number }
const memStore = new Map<string, Entry>()

function checkMemory(key: string, max: number, windowSec: number): boolean {
  const now = Date.now()
  const entry = memStore.get(key)
  if (!entry || now > entry.resetAt) {
    memStore.set(key, { count: 1, resetAt: now + windowSec * 1000 })
    return true
  }
  if (entry.count >= max) return false
  entry.count++
  return true
}

async function checkRedis(r: Redis, key: string, max: number, windowSec: number): Promise<boolean> {
  const count = await r.incr(key)
  if (count === 1) await r.expire(key, windowSec)
  return count <= max
}

export default defineEventHandler(async (event) => {
  const path = event.path
  const limit = LIMITS[path]
  if (!limit) return

  const ip = getRequestIP(event, { xForwardedFor: true }) ?? 'unknown'
  const key = `rl:${path}:${ip}`

  const r = getRedis()
  const allowed = r
    ? await checkRedis(r, key, limit.max, limit.windowSec).catch(() => checkMemory(key, limit.max, limit.windowSec))
    : checkMemory(key, limit.max, limit.windowSec)

  if (!allowed) {
    throw createError({
      statusCode: 429,
      message: 'Trop de requêtes. Veuillez réessayer plus tard.'
    })
  }
})
