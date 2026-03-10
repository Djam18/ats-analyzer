<script setup lang="ts">
const props = defineProps<{ score: number }>()

const { getScoreColor, getScoreLabel } = useAnalysis()

// SVG circle gauge
const radius = 54
const circumference = 2 * Math.PI * radius
const dashOffset = computed(() =>
  circumference - (props.score / 100) * circumference
)

const strokeColor = computed(() => {
  if (props.score >= 71) return '#22c55e'
  if (props.score >= 41) return '#f97316'
  return '#ef4444'
})
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="relative w-40 h-40">
      <svg class="w-40 h-40 -rotate-90" viewBox="0 0 128 128">
        <!-- Background circle -->
        <circle
          cx="64"
          cy="64"
          :r="radius"
          fill="none"
          stroke="currentColor"
          class="text-gray-200 dark:text-gray-700"
          stroke-width="12"
        />
        <!-- Progress circle -->
        <circle
          cx="64"
          cy="64"
          :r="radius"
          fill="none"
          :stroke="strokeColor"
          stroke-width="12"
          stroke-linecap="round"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="dashOffset"
          class="transition-all duration-700 ease-out"
        />
      </svg>
      <!-- Score label inside -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <span class="text-4xl font-bold" :class="getScoreColor(score)">{{ score }}</span>
        <span class="text-xs text-gray-400 font-medium">/100</span>
      </div>
    </div>
    <div
      class="mt-3 px-4 py-1 rounded-full text-sm font-semibold"
      :class="score >= 71
        ? 'bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-400'
        : score >= 41
          ? 'bg-orange-100 text-orange-700 dark:bg-orange-950 dark:text-orange-400'
          : 'bg-red-100 text-red-700 dark:bg-red-950 dark:text-red-400'"
    >
      {{ getScoreLabel(score) }}
    </div>
  </div>
</template>
