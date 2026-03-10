<script setup lang="ts">
const { quota, fetchQuota, remainingLabel, isLow, percentage } = useQuota()

onMounted(fetchQuota)
</script>

<template>
  <UCard>
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-zap" class="w-5 h-5 text-primary" />
        <span class="font-semibold text-gray-900 dark:text-white text-sm">Analyses disponibles</span>
      </div>
      <UBadge
        v-if="quota"
        :color="quota.plan === 'free' ? 'neutral' : 'primary'"
        variant="soft"
        size="sm"
        class="capitalize"
      >
        {{ quota.plan }}
      </UBadge>
    </div>

    <div v-if="quota">
      <div class="flex items-end justify-between mb-2">
        <span
          class="text-2xl font-bold"
          :class="isLow ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-white'"
        >
          {{ quota.plan === 'expert' ? '∞' : quota.remaining }}
        </span>
        <span class="text-sm text-gray-400">{{ remainingLabel }}</span>
      </div>

      <div v-if="quota.plan !== 'expert'" class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <div
          class="h-2 rounded-full transition-all duration-500"
          :class="isLow ? 'bg-red-500' : 'bg-primary'"
          :style="{ width: `${percentage}%` }"
        />
      </div>

      <div v-if="isLow" class="mt-3 flex items-center gap-2">
        <UIcon name="i-lucide-alert-triangle" class="w-4 h-4 text-orange-500" />
        <span class="text-xs text-orange-600 dark:text-orange-400">
          Il ne vous reste plus qu'une analyse.
        </span>
      </div>

      <UButton
        v-if="quota.plan === 'free' && quota.remaining === 0"
        to="/pricing"
        size="sm"
        class="w-full mt-3"
      >
        Passer au plan Pro
      </UButton>
    </div>

    <div v-else class="h-16 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
  </UCard>
</template>
