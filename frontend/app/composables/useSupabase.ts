import { createClient } from '@supabase/supabase-js'
import type { Database } from '~/types/database'

let _client: ReturnType<typeof createClient<Database>> | null = null

export function useSupabase() {
  if (_client) return _client

  const config = useRuntimeConfig()

  _client = createClient<Database>(
    config.public.supabaseUrl,
    config.public.supabaseAnonKey,
    {
      db: { schema: 'ats' },
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        storageKey: 'ats-auth',
      },
    },
  )

  return _client
}
