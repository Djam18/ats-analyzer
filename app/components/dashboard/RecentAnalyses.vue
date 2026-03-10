<script setup lang="ts">
import type { Analysis } from '~/composables/useAnalysis'

const { fetchAnalyses } = useAnalysis()

const analyses = ref<Analysis[]>([])
const loading = ref(true)

onMounted(async () => {
  const result = await fetchAnalyses(1)
  analyses.value = result.data.slice(0, 5)
  loading.value = false
})
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
        Analyses récentes
      </h2>
      <NuxtLink
        v-if="analyses.length > 0"
        to="/analyses"
        class="text-sm text-primary hover:underline"
      >
        Voir tout
      </NuxtLink>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="h-20 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
    </div>

    <SharedEmptyState
      v-else-if="analyses.length === 0"
      icon="i-lucide-scan-text"
      title="Aucune analyse effectuée"
      description="Lancez votre première analyse ATS pour découvrir votre score de compatibilité."
      action-label="Nouvelle analyse"
      action-to="/analyses/new"
    />

    <div v-else class="space-y-3">
      <AnalysisCard
        v-for="analysis in analyses"
        :key="analysis.id"
        :analysis="analysis"
      />
    </div>
  </div>
</template>
