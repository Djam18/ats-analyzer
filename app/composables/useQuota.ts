export interface QuotaInfo {
  allowed: boolean
  remaining: number
  plan: string
  used: number
  subscription_status: string | null
}

export const useQuota = () => {
  const quota = useState<QuotaInfo | null>('quota', () => null)
  const loading = ref(false)

  async function fetchQuota() {
    loading.value = true
    try {
      quota.value = await $fetch<QuotaInfo>('/api/user/quota')
    }
    catch {
      quota.value = null
    }
    finally {
      loading.value = false
    }
  }

  const remainingLabel = computed(() => {
    if (!quota.value) return ''
    if (quota.value.plan === 'expert') return 'Illimité'
    if (quota.value.plan === 'pro') return `${quota.value.remaining} / 50 ce mois`
    return `${quota.value.remaining} / 3 gratuites`
  })

  const isLow = computed(() =>
    quota.value ? quota.value.remaining <= 1 && quota.value.plan !== 'expert' : false
  )

  const percentage = computed(() => {
    if (!quota.value || quota.value.plan === 'expert') return 100
    if (quota.value.plan === 'pro') return Math.round((quota.value.remaining / 50) * 100)
    return Math.round((quota.value.remaining / 3) * 100)
  })

  return { quota, loading, fetchQuota, remainingLabel, isLow, percentage }
}
