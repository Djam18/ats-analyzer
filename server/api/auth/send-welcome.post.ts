import { serverSupabaseUser } from '#supabase/server'
import { sendWelcomeEmail } from '../../utils/email'

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const supabase = useServerSupabase()
  const { data: profile } = await supabase
    .from('profiles')
    .select('full_name, welcome_email_sent')
    .eq('id', user.id)
    .single()

  // Idempotent: only send once
  if ((profile as any)?.welcome_email_sent) {
    return { sent: false, reason: 'already_sent' }
  }

  const name = (profile as any)?.full_name || user.email?.split('@')[0] || 'utilisateur'
  const email = user.email!

  try {
    await sendWelcomeEmail(email, name)
    await supabase
      .from('profiles')
      .update({ welcome_email_sent: true } as any)
      .eq('id', user.id)
  }
  catch (err) {
    // Non-blocking: log but don't fail the request
    console.error('Failed to send welcome email:', err)
  }

  return { sent: true }
})
