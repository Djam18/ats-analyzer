<script setup lang="ts">
import type { Analysis } from '~/composables/useAnalysis'

defineProps<{ analysis: Analysis }>()

const { getScoreColor, getScoreLabel, getScoreBg } = useAnalysis()

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
}
</script>

<template>
  <NuxtLink
    :to="`/analyses/${analysis.id}`"
    class="block border border-gray-200 dark:border-gray-700 rounded-xl p-4 hover:border-primary hover:shadow-sm transition-all duration-200"
  >
    <div class="flex items-center gap-4">
      <!-- Score badge -->
      <div class="flex-shrink-0">
        <div v-if="analysis.status === 'completed' && analysis.score !== null" class="text-center">
          <div
            class="w-14 h-14 rounded-full flex items-center justify-center border-4"
            :class="analysis.score >= 71
              ? 'border-green-400 bg-green-50 dark:bg-green-950'
              : analysis.score >= 41
                ? 'border-orange-400 bg-orange-50 dark:bg-orange-950'
                : 'border-red-400 bg-red-50 dark:bg-red-950'"
          >
            <span class="text-lg font-bold" :class="getScoreColor(analysis.score)">
              {{ analysis.score }}
            </span>
          </div>
        </div>
        <div v-else-if="analysis.status === 'processing' || analysis.status === 'pending'" class="w-14 h-14 rounded-full border-4 border-gray-200 dark:border-gray-700 flex items-center justify-center">
          <UIcon name="i-lucide-loader-2" class="w-6 h-6 animate-spin text-gray-400" />
        </div>
        <div v-else class="w-14 h-14 rounded-full border-4 border-red-200 bg-red-50 dark:bg-red-950 flex items-center justify-center">
          <UIcon name="i-lucide-x" class="w-6 h-6 text-red-500" />
        </div>
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <p class="font-semibold text-gray-900 dark:text-white truncate">
          {{ analysis.job_title }}
        </p>
        <p v-if="analysis.company_name" class="text-sm text-gray-500 dark:text-gray-400 truncate">
          {{ analysis.company_name }}
        </p>
        <div class="flex items-center gap-3 mt-1">
          <span class="text-xs text-gray-400">{{ formatDate(analysis.created_at) }}</span>
          <span
            v-if="analysis.status === 'completed' && analysis.score !== null"
            class="text-xs font-medium"
            :class="getScoreColor(analysis.score)"
          >
            {{ getScoreLabel(analysis.score) }}
          </span>
          <UBadge v-else-if="analysis.status === 'failed'" color="error" variant="soft" size="xs">
            Échoué
          </UBadge>
        </div>
      </div>

      <UIcon name="i-lucide-chevron-right" class="w-5 h-5 text-gray-400 flex-shrink-0" />
    </div>
  </NuxtLink>
</template>
