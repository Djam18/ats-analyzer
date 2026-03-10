import { Resend } from 'resend'

function escapeHtml(str: string): string {
  return str.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c] ?? c))
}

let resendClient: Resend | null = null

function getClient(): Resend {
  if (resendClient) return resendClient
  resendClient = new Resend(process.env.RESEND_API_KEY)
  return resendClient
}

const FROM = 'ATS Analyzer <noreply@ats-analyzer.app>'

export async function sendWelcomeEmail(to: string, rawName: string): Promise<void> {
  const name = escapeHtml(rawName)
  const resend = getClient()
  await resend.emails.send({
    from: FROM,
    to,
    subject: 'Bienvenue sur ATS Analyzer !',
    html: `
      <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 32px;">
        <h1 style="color: #4f46e5; margin-bottom: 8px;">Bienvenue, ${name} !</h1>
        <p style="color: #6b7280; font-size: 16px; line-height: 1.6;">
          Votre compte ATS Analyzer est prêt. Vous disposez de <strong>3 analyses gratuites</strong>
          pour découvrir la compatibilité de votre CV avec vos offres d'emploi cibles.
        </p>
        <div style="margin: 32px 0;">
          <a
            href="${process.env.NUXT_PUBLIC_APP_URL ?? 'http://localhost:3000'}/onboarding"
            style="background: #4f46e5; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;"
          >
            Commencer maintenant
          </a>
        </div>
        <p style="color: #9ca3af; font-size: 14px;">
          Pour toute question, répondez simplement à cet email.
        </p>
      </div>
    `
  })
}

export async function sendQuotaWarningEmail(to: string, rawName: string): Promise<void> {
  const name = escapeHtml(rawName)
  const resend = getClient()
  await resend.emails.send({
    from: FROM,
    to,
    subject: 'Il vous reste 1 analyse gratuite',
    html: `
      <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 32px;">
        <h1 style="color: #f97316; margin-bottom: 8px;">Dernière analyse gratuite, ${name}</h1>
        <p style="color: #6b7280; font-size: 16px; line-height: 1.6;">
          Il ne vous reste plus qu'<strong>1 analyse gratuite</strong>.
          Passez au plan Pro pour continuer à optimiser votre CV sans interruption.
        </p>
        <div style="margin: 32px 0;">
          <a
            href="${process.env.NUXT_PUBLIC_APP_URL ?? 'http://localhost:3000'}/pricing"
            style="background: #4f46e5; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600;"
          >
            Voir les plans
          </a>
        </div>
      </div>
    `
  })
}
