export const useSubscription = () => {
  const toast = useToast()
  const loading = ref(false)

  async function redirectToCheckout(plan: 'pro' | 'expert') {
    loading.value = true
    try {
      const { url } = await $fetch<{ url: string }>('/api/stripe/create-checkout', {
        method: 'POST',
        body: { plan }
      })
      window.location.href = url
    }
    catch (err: unknown) {
      const message = (err as { data?: { message?: string } })?.data?.message ?? 'Erreur de paiement'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
    }
    finally {
      loading.value = false
    }
  }

  async function redirectToPortal() {
    loading.value = true
    try {
      const { url } = await $fetch<{ url: string }>('/api/stripe/create-portal', { method: 'POST' })
      window.location.href = url
    }
    catch (err: unknown) {
      const message = (err as { data?: { message?: string } })?.data?.message ?? 'Erreur portail'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
    }
    finally {
      loading.value = false
    }
  }

  return { loading, redirectToCheckout, redirectToPortal }
}
