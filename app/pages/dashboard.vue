<script setup lang="ts">
definePageMeta({ middleware: ['auth', 'onboarding'] })

const { t } = useI18n()
const user = useSupabaseUser()

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return t('dashboard.greeting.morning')
  if (hour < 18) return t('dashboard.greeting.afternoon')
  return t('dashboard.greeting.evening')
})

const firstName = computed(() => {
  const name = user.value?.user_metadata?.full_name as string | undefined
  return name?.split(' ')[0] ?? 'vous'
})
</script>

<template>
  <div>
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ greeting }}, {{ firstName }}
      </h1>
      <p class="text-gray-500 dark:text-gray-400 mt-1">
        {{ t('dashboard.subtitle') }}
      </p>
    </div>

    <UCard class="mb-6 bg-gradient-to-r from-primary-600 to-primary-500">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-white font-semibold text-lg mb-1">
            {{ t('dashboard.cta.title') }}
          </h2>
          <p class="text-primary-100 text-sm">
            {{ t('dashboard.cta.subtitle') }}
          </p>
        </div>
        <UButton
          to="/analyses/new"
          color="neutral"
          variant="solid"
          icon="i-lucide-scan-text"
          class="flex-shrink-0"
        >
          {{ t('dashboard.cta.button') }}
        </UButton>
      </div>
    </UCard>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <DashboardQuotaIndicator class="md:col-span-1" />

      <UCard class="md:col-span-1">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-100 dark:bg-blue-950 rounded-lg flex items-center justify-center">
            <UIcon name="i-lucide-file-text" class="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <p class="text-sm text-gray-500">
              {{ t('dashboard.quickLinks.cvs') }}
            </p>
            <NuxtLink to="/cvs" class="font-semibold text-gray-900 dark:text-white hover:text-primary text-sm">
              {{ t('dashboard.quickLinks.manageCvs') }} →
            </NuxtLink>
          </div>
        </div>
      </UCard>

      <UCard class="md:col-span-1">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-purple-100 dark:bg-purple-950 rounded-lg flex items-center justify-center">
            <UIcon name="i-lucide-history" class="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <p class="text-sm text-gray-500">
              {{ t('dashboard.quickLinks.history') }}
            </p>
            <NuxtLink to="/analyses" class="font-semibold text-gray-900 dark:text-white hover:text-primary text-sm">
              {{ t('dashboard.quickLinks.viewAll') }} →
            </NuxtLink>
          </div>
        </div>
      </UCard>
    </div>

    <DashboardRecentAnalyses />
  </div>
</template>
