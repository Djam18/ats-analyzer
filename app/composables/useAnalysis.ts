export interface Analysis {
  id: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
  score: number | null
  job_title: string
  company_name: string | null
  created_at: string
  completed_at: string | null
  matched_keywords: Array<{ keyword: string, context?: string }> | null
  missing_keywords: Array<{ keyword: string, importance: 'high' | 'medium' | 'low' }> | null
  analysis_details: {
    sections_analysis: {
      experience: { score: number, feedback: string }
      skills: { score: number, feedback: string }
      education: { score: number, feedback: string }
      formatting: { score: number, feedback: string }
    }
    suggestions: Array<{ original: string, improved: string, reason: string }>
    seniority_match: { cv_level: string, job_level: string, match: boolean }
    summary: string
  } | null
  error_message: string | null
  cvs?: { id: string, display_name: string, file_type: string } | null
}

export const useAnalysis = () => {
  const toast = useToast()
  const { fetchQuota } = useQuota()

  async function createAnalysis(params: {
    cv_id: string
    job_title: string
    company_name?: string
    job_description: string
  }): Promise<{ id: string } | null> {
    try {
      const data = await $fetch<{ id: string, status: string }>('/api/analysis/create', {
        method: 'POST',
        body: params
      })
      // Refresh quota after successful analysis
      await fetchQuota()
      return data
    }
    catch (error: unknown) {
      const err = error as { data?: { message?: string }, status?: number }
      const message = err?.data?.message ?? 'L\'analyse a échoué. Réessayez.'
      const isQuotaError = err?.status === 402

      toast.add({
        title: isQuotaError ? 'Quota épuisé' : 'Analyse échouée',
        description: message,
        color: isQuotaError ? 'warning' : 'error',
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ...(isQuotaError ? { actions: [{ label: 'Voir les plans', onClick: () => navigateTo('/pricing') }] as any } : {})
      })
      return null
    }
  }

  async function fetchAnalysis(id: string): Promise<Analysis | null> {
    try {
      return await $fetch<Analysis>(`/api/analysis/${id}`)
    }
    catch {
      return null
    }
  }

  async function fetchAnalyses(page = 1): Promise<{ data: Analysis[], meta: { total: number, pages: number } }> {
    try {
      return await $fetch(`/api/analysis?page=${page}`)
    }
    catch {
      return { data: [], meta: { total: 0, pages: 0 } }
    }
  }

  function getScoreColor(score: number): string {
    if (score >= 71) return 'text-green-600 dark:text-green-400'
    if (score >= 41) return 'text-orange-500 dark:text-orange-400'
    return 'text-red-600 dark:text-red-400'
  }

  function getScoreLabel(score: number): string {
    if (score >= 71) return 'Excellent'
    if (score >= 41) return 'Moyen'
    return 'Faible'
  }

  function getScoreBg(score: number): string {
    if (score >= 71) return 'bg-green-500'
    if (score >= 41) return 'bg-orange-500'
    return 'bg-red-500'
  }

  return {
    createAnalysis,
    fetchAnalysis,
    fetchAnalyses,
    getScoreColor,
    getScoreLabel,
    getScoreBg
  }
}
