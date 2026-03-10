<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { t } = useI18n()
const { quota, fetchQuota } = useQuota()
const { redirectToPortal, loading } = useSubscription()

onMounted(fetchQuota)

const planLabels = computed(() => ({
  free: t('quota.plan.free'),
  pro: `${t('quota.plan.pro')} — 9.99€/mois`,
  expert: `${t('quota.plan.expert')} — 19.99€/mois`
}))

const currentPlanLabel = computed(() =>
  (planLabels.value as Record<string, string>)[quota.value?.plan ?? 'free'] ?? quota.value?.plan ?? ''
)

const statusLabels = computed<Record<string, { label: string, color: 'success' | 'warning' | 'error' | 'neutral' }>>(() => ({
  active: { label: t('settings.billing.status.active'), color: 'success' },
  past_due: { label: t('settings.billing.status.past_due'), color: 'warning' },
  canceled: { label: t('settings.billing.status.canceled'), color: 'error' }
}))
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ t('settings.billing.title') }}
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        {{ t('settings.billing.subtitle') }}
      </p>
    </div>

    <UCard class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="font-semibold text-gray-900 dark:text-white">
          {{ t('settings.billing.currentPlan') }}
        </h2>
        <UBadge
          v-if="quota?.subscription_status"
          :color="statusLabels[quota.subscription_status]?.color ?? 'neutral'"
          variant="soft"
        >
          {{ statusLabels[quota.subscription_status]?.label }}
        </UBadge>
      </div>

      <div v-if="quota" class="space-y-4">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-primary-100 dark:bg-primary-950 rounded-xl flex items-center justify-center">
            <UIcon name="i-lucide-zap" class="w-6 h-6 text-primary" />
          </div>
          <div>
            <p class="font-bold text-lg text-gray-900 dark:text-white">
              {{ currentPlanLabel }}
            </p>
            <p class="text-sm text-gray-500">
              {{ quota.plan === 'expert' ? t('quota.expert') : quota.plan === 'pro' ? t('quota.pro', { remaining: quota.remaining }) : t('quota.free', { remaining: quota.remaining }) }}
            </p>
          </div>
        </div>

        <div v-if="quota.plan === 'free'" class="flex gap-3 pt-2">
          <UButton to="/pricing" icon="i-lucide-arrow-up-circle">
            {{ t('quota.upgrade') }}
          </UButton>
        </div>

        <div v-else class="flex gap-3 pt-2">
          <UButton
            variant="outline"
            color="neutral"
            icon="i-lucide-settings"
            :loading="loading"
            @click="redirectToPortal"
          >
            {{ t('settings.billing.manage') }}
          </UButton>
          <p class="text-xs text-gray-400 self-center">
            {{ t('settings.billing.manageHint') }}
          </p>
        </div>
      </div>

      <div v-else class="h-24 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
    </UCard>

    <UCard v-if="quota && quota.plan !== 'free'">
      <div class="flex items-start gap-3">
        <UIcon name="i-lucide-info" class="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
        <div>
          <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            {{ t('settings.billing.cancel') }}
          </p>
          <p class="text-sm text-gray-500">
            {{ t('settings.billing.cancelNote') }}
          </p>
          <UButton
            variant="ghost"
            color="error"
            size="sm"
            class="mt-3"
            :loading="loading"
            @click="redirectToPortal"
          >
            {{ t('settings.billing.cancel') }}
          </UButton>
        </div>
      </div>
    </UCard>
  </div>
</template>
