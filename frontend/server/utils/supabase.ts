import { createClient } from '@supabase/supabase-js'
import type { Database } from '../../../app/types/database'

/**
 * Service-role Supabase client for server-side endpoints.
 * Bypasses RLS — use only in trusted server routes.
 */
export function useSupabaseAdmin() {
  const config = useRuntimeConfig()

  return createClient<Database>(
    config.public.supabaseUrl,
    config.supabaseServiceKey,
    {
      db: { schema: 'ats' },
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    },
  )
}
