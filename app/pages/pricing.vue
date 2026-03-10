<script setup lang="ts">
const { t } = useI18n()
const user = useSupabaseUser()
const { quota } = useQuota()

const plans = computed(() => [
  {
    id: 'free',
    name: t('quota.plan.free'),
    price: 0,
    features: [t('pricing.features.analyses3'), t('pricing.features.scoreAndKeywords'), t('pricing.features.basicSuggestions')],
    missing: [],
    cta: t('pricing.cta.free'),
    highlight: false
  },
  {
    id: 'pro',
    name: t('quota.plan.pro'),
    price: 9.99,
    features: [t('pricing.features.analyses50'), t('pricing.features.fullAnalysis'), t('pricing.features.unlimitedHistory'), t('pricing.features.emailSupport')],
    missing: [],
    cta: t('pricing.cta.pro'),
    priceId: 'pro',
    highlight: true
  },
  {
    id: 'expert',
    name: t('quota.plan.expert'),
    price: 19.99,
    features: [t('pricing.features.analysesUnlimited'), t('pricing.features.fullAnalysis'), t('pricing.features.unlimitedHistory'), t('pricing.features.prioritySupport')],
    missing: [],
    cta: t('pricing.cta.expert'),
    priceId: 'expert',
    highlight: false
  }
])

const subscribing = ref<string | null>(null)
const currentPlan = computed(() => quota.value?.plan ?? 'free')

async function handleSubscribe(planId: string) {
  if (!user.value) {
    await navigateTo('/register')
    return
  }
  if (planId === 'free') return

  subscribing.value = planId
  try {
    const { url } = await $fetch<{ url: string }>('/api/stripe/create-checkout', {
      method: 'POST',
      body: { plan: planId }
    })
    window.location.href = url
  }
  catch (err: unknown) {
    const message = (err as { data?: { message?: string } })?.data?.message ?? t('common.error')
    useToast().add({ title: t('common.error'), description: message, color: 'error' })
  }
  finally {
    subscribing.value = null
  }
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 py-12">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
        {{ t('pricing.title') }}
      </h1>
      <p class="text-lg text-gray-500 dark:text-gray-400">
        {{ t('pricing.subtitle') }}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div
        v-for="plan in plans"
        :key="plan.id"
        class="relative flex flex-col rounded-2xl border-2 p-6 transition-all"
        :class="plan.highlight
          ? 'border-primary shadow-lg shadow-primary/10 scale-[1.02]'
          : 'border-gray-200 dark:border-gray-700'"
      >
        <div
          v-if="plan.highlight"
          class="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-white text-xs font-bold px-4 py-1.5 rounded-full"
        >
          {{ t('pricing.popular') }}
        </div>

        <UBadge
          v-if="currentPlan === plan.id"
          color="success"
          variant="soft"
          class="self-start mb-3"
        >
          {{ t('pricing.currentPlan') }}
        </UBadge>

        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-1">
          {{ plan.name }}
        </h2>

        <div class="mb-6 mt-3">
          <span class="text-4xl font-bold text-gray-900 dark:text-white">
            {{ plan.price === 0 ? t('quota.plan.free') : `${plan.price}€` }}
          </span>
          <span v-if="plan.price > 0" class="text-gray-400 text-sm">
            /{{ t('pricing.monthly') }}
          </span>
        </div>

        <UButton
          class="w-full mb-6"
          :color="plan.highlight ? 'primary' : 'neutral'"
          :variant="plan.highlight ? 'solid' : 'outline'"
          :loading="subscribing === plan.id"
          :disabled="currentPlan === plan.id || (plan.id === 'free' && !!user)"
          @click="handleSubscribe(plan.id)"
        >
          {{ currentPlan === plan.id ? t('pricing.currentPlan') : plan.cta }}
        </UButton>

        <ul class="space-y-2.5 flex-1">
          <li
            v-for="feature in plan.features"
            :key="feature"
            class="flex items-center gap-2.5 text-sm"
          >
            <UIcon name="i-lucide-check" class="w-4 h-4 text-green-500 flex-shrink-0" />
            <span class="text-gray-700 dark:text-gray-300">{{ feature }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
