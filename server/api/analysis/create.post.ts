import { serverSupabaseUser } from '#supabase/server'
import { z } from 'zod'
import { checkQuota, consumeQuota, refundQuota } from '../../utils/quota'
import { analyzeAts } from '../../utils/huggingface'
import { sendQuotaWarningEmail } from '../../utils/email'

const schema = z.object({
  cv_id: z.string().uuid(),
  job_title: z.string().min(2).max(200),
  company_name: z.string().max(200).nullable().optional(),
  job_description: z.string().min(100).max(10000)
})

export default defineEventHandler(async (event) => {
  const user = await serverSupabaseUser(event)
  if (!user) {
    throw createError({ statusCode: 401, message: 'Non authentifié' })
  }

  const body = await readBody(event)
  const parsed = schema.safeParse(body)
  if (!parsed.success) {
    throw createError({
      statusCode: 422,
      message: parsed.error.errors[0]?.message ?? 'Données invalides'
    })
  }

  const { cv_id, job_title, company_name, job_description } = parsed.data
  const supabase = useServerSupabase()

  // Check quota BEFORE creating the analysis
  const quota = await checkQuota(supabase, user.id)
  if (!quota.allowed) {
    throw createError({
      statusCode: 402,
      message: quota.plan === 'free'
        ? 'Vous avez utilisé vos 3 analyses gratuites. Passez au plan Pro pour continuer.'
        : 'Quota mensuel atteint. Passez au plan Expert pour des analyses illimitées.'
    })
  }

  // Verify CV ownership and get extracted text
  const { data: cv, error: cvError } = await supabase
    .from('cvs')
    .select('id, extracted_text, is_scanned, display_name')
    .eq('id', cv_id)
    .eq('user_id', user.id)
    .single()

  if (cvError || !cv) {
    throw createError({ statusCode: 404, message: 'CV introuvable' })
  }

  if (!cv.extracted_text) {
    throw createError({
      statusCode: 422,
      message: 'Ce CV ne contient pas de texte analysable. Uploadez un PDF avec du texte sélectionnable.'
    })
  }

  // Consume quota BEFORE analysis to prevent race condition bypass
  await consumeQuota(supabase, user.id, quota.plan)

  // Create analysis record in pending state
  const { data: analysis, error: createError_ } = await supabase
    .from('analyses')
    .insert({
      user_id: user.id,
      cv_id,
      job_title,
      company_name: company_name ?? null,
      job_description,
      status: 'processing'
    })
    .select('id')
    .single()

  if (createError_ || !analysis) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la création de l\'analyse' })
  }

  const analysisId = analysis.id

  // Run ATS analysis (inline, no queue needed for MVP)
  // Use event.waitUntil equivalent: run async, update DB when done
  let atsResult
  try {
    atsResult = await analyzeAts({
      cvText: cv.extracted_text,
      jobTitle: job_title,
      companyName: company_name ?? null,
      jobDescription: job_description
    })
  }
  catch (err: unknown) {
    // Mark as failed and refund quota (consumed optimistically above)
    await Promise.all([
      supabase
        .from('analyses')
        .update({
          status: 'failed',
          error_message: err instanceof Error ? err.message : 'Erreur inconnue'
        })
        .eq('id', analysisId),
      refundQuota(supabase, user.id, quota.plan)
    ])

    throw createError({
      statusCode: 502,
      message: err instanceof Error ? err.message : 'L\'analyse a échoué. Réessayez.'
    })
  }

  // Save results and mark as completed
  const { error: updateError } = await supabase
    .from('analyses')
    .update({
      status: 'completed',
      score: atsResult.score,
      matched_keywords: atsResult.matched_keywords,
      missing_keywords: atsResult.missing_keywords,
      analysis_details: {
        sections_analysis: atsResult.sections_analysis,
        suggestions: atsResult.suggestions,
        seniority_match: atsResult.seniority_match,
        summary: atsResult.summary
      },
      completed_at: new Date().toISOString()
    })
    .eq('id', analysisId)

  if (updateError) {
    throw createError({ statusCode: 500, message: 'Erreur lors de la sauvegarde des résultats' })
  }

  // Send quota warning email when free plan user has 1 analysis left (non-blocking)
  if (quota.plan === 'free' && quota.remaining - 1 === 1) {
    const { data: profile } = await supabase
      .from('profiles')
      .select('full_name')
      .eq('id', user.id)
      .single()
    const name = (profile as any)?.full_name || user.email?.split('@')[0] || 'utilisateur'
    if (user.email) {
      sendQuotaWarningEmail(user.email, name).catch(err =>
        console.error('Failed to send quota warning email:', err)
      )
    }
  }

  return { id: analysisId, status: 'completed' }
})
