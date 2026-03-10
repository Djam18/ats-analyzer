<script setup lang="ts">
defineProps<{
  keywords: Array<{ keyword: string, importance: 'high' | 'medium' | 'low' }>
}>()

const importanceConfig = {
  high: { label: 'Critique', class: 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300', dot: 'bg-red-500' },
  medium: { label: 'Important', class: 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300', dot: 'bg-orange-500' },
  low: { label: 'Optionnel', class: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400', dot: 'bg-gray-400' }
}
</script>

<template>
  <div>
    <div class="flex items-center gap-2 mb-3">
      <UIcon name="i-lucide-x-circle" class="w-5 h-5 text-red-500" />
      <h3 class="font-semibold text-gray-900 dark:text-white">
        Mots-clés manquants
      </h3>
      <UBadge color="error" variant="soft" size="sm">
        {{ keywords.length }}
      </UBadge>
    </div>

    <div v-if="keywords.length === 0" class="text-sm text-gray-400 italic">
      Aucun mot-clé manquant. Excellent !
    </div>

    <div v-else>
      <!-- Legend -->
      <div class="flex items-center gap-4 mb-3 text-xs text-gray-400">
        <span v-for="(cfg, key) in importanceConfig" :key="key" class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full" :class="cfg.dot" />
          {{ cfg.label }}
        </span>
      </div>

      <div class="flex flex-wrap gap-2">
        <span
          v-for="kw in keywords"
          :key="kw.keyword"
          class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium"
          :class="importanceConfig[kw.importance].class"
        >
          <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" :class="importanceConfig[kw.importance].dot" />
          {{ kw.keyword }}
        </span>
      </div>
    </div>
  </div>
</template>
