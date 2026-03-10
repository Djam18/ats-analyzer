<script setup lang="ts">
import type { Analysis } from '~/composables/useAnalysis'

definePageMeta({ middleware: ['auth', 'onboarding'] })

const { fetchAnalyses } = useAnalysis()

const analyses = ref<Analysis[]>([])
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(1)
const total = ref(0)

async function load(page = 1) {
  loading.value = true
  const result = await fetchAnalyses(page)
  analyses.value = result.data
  totalPages.value = result.meta.pages
  total.value = result.meta.total
  currentPage.value = page
  loading.value = false
}

onMounted(() => load(1))
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          Historique des analyses
        </h1>
        <p class="text-sm text-gray-500 mt-1">
          {{ total }} analyse{{ total > 1 ? 's' : '' }} au total
        </p>
      </div>
      <UButton to="/analyses/new" icon="i-lucide-plus">
        Nouvelle analyse
      </UButton>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-20 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
    </div>

    <SharedEmptyState
      v-else-if="analyses.length === 0"
      icon="i-lucide-scan-text"
      title="Aucune analyse effectuée"
      description="Lancez votre première analyse ATS pour voir votre compatibilité avec des offres d'emploi."
      action-label="Lancer une analyse"
      action-to="/analyses/new"
    />

    <div v-else class="space-y-3">
      <AnalysisCard
        v-for="analysis in analyses"
        :key="analysis.id"
        :analysis="analysis"
      />

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center pt-4">
        <UPagination
          v-model:page="currentPage"
          :total="total"
          :items-per-page="20"
          @update:page="load"
        />
      </div>
    </div>
  </div>
</template>
