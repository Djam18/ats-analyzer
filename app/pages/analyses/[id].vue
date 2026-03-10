<script setup lang="ts">
import type { Analysis } from '~/composables/useAnalysis'

definePageMeta({ middleware: ['auth', 'onboarding'] })

const { t } = useI18n()
const toast = useToast()
const route = useRoute()
const { fetchAnalysis, getScoreColor, getScoreLabel } = useAnalysis()

const analysis = ref<Analysis | null>(null)
const loading = ref(true)
const error = ref(false)

onMounted(async () => {
  const data = await fetchAnalysis(route.params.id as string)
  if (!data) {
    error.value = true
  }
  else {
    analysis.value = data
  }
  loading.value = false
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('fr-FR', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })
}

async function copyToClipboard(text: string) {
  const toast = useToast()
  try {
    await navigator.clipboard.writeText(text)
    toast.add({ title: t('analysis.suggestions.copy'), color: 'success', duration: 2000 })
  }
  catch {
    toast.add({ title: t('common.error'), color: 'error', duration: 2000 })
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <!-- Loading -->
    <div v-if="loading" class="space-y-6">
      <div class="h-8 w-64 bg-gray-100 dark:bg-gray-800 rounded animate-pulse" />
      <div class="h-48 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
      <div class="h-48 bg-gray-100 dark:bg-gray-800 rounded-xl animate-pulse" />
    </div>

    <!-- Error -->
    <SharedEmptyState
      v-else-if="error || !analysis"
      icon="i-lucide-x-circle"
      title="Analyse introuvable"
      description="Cette analyse n'existe pas ou vous n'y avez pas accès."
      action-label="Retour à l'historique"
      action-to="/analyses"
    />

    <!-- Results -->
    <template v-else>
      <!-- Header -->
      <div class="mb-6">
        <NuxtLink to="/analyses" class="flex items-center gap-1 text-sm text-gray-500 hover:text-primary mb-3">
          <UIcon name="i-lucide-arrow-left" class="w-4 h-4" />
          Retour à l'historique
        </NuxtLink>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ analysis.job_title }}
        </h1>
        <div class="flex items-center gap-3 mt-1 text-sm text-gray-500">
          <span v-if="analysis.company_name">{{ analysis.company_name }}</span>
          <span v-if="analysis.company_name">·</span>
          <span>{{ formatDate(analysis.created_at) }}</span>
          <span v-if="analysis.cvs">·</span>
          <span v-if="analysis.cvs" class="flex items-center gap-1">
            <UIcon name="i-lucide-file-text" class="w-3 h-3" />
            {{ analysis.cvs.display_name }}
          </span>
        </div>
      </div>

      <!-- Score hero -->
      <UCard class="mb-6 text-center">
        <div class="py-4">
          <AnalysisScoreGauge v-if="analysis.score !== null" :score="analysis.score" />
          <p v-if="analysis.analysis_details?.summary" class="mt-4 text-sm text-gray-500 dark:text-gray-400 max-w-xl mx-auto">
            {{ analysis.analysis_details.summary }}
          </p>
        </div>
      </UCard>

      <!-- Keywords -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <UCard>
          <AnalysisMatchedKeywords
            :keywords="analysis.matched_keywords ?? []"
          />
        </UCard>
        <UCard>
          <AnalysisMissingKeywords
            :keywords="analysis.missing_keywords ?? []"
          />
        </UCard>
      </div>

      <!-- Section scores -->
      <UCard v-if="analysis.analysis_details?.sections_analysis" class="mb-6">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <UIcon name="i-lucide-bar-chart-2" class="w-5 h-5 text-primary" />
          Analyse par section
        </h3>
        <div class="space-y-4">
          <div
            v-for="(section, key) in analysis.analysis_details.sections_analysis"
            :key="key"
          >
            <div class="flex items-center justify-between mb-1">
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                {{ { experience: 'Expérience', skills: 'Compétences', education: 'Formation', formatting: 'Format' }[key] }}
              </span>
              <span class="text-sm font-bold" :class="getScoreColor(section.score)">
                {{ section.score }}/100
              </span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-1">
              <div
                class="h-2 rounded-full transition-all duration-500"
                :class="section.score >= 71 ? 'bg-green-500' : section.score >= 41 ? 'bg-orange-500' : 'bg-red-500'"
                :style="{ width: `${section.score}%` }"
              />
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ section.feedback }}
            </p>
          </div>
        </div>
      </UCard>

      <!-- Suggestions -->
      <UCard v-if="analysis.analysis_details?.suggestions?.length" class="mb-6">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <UIcon name="i-lucide-lightbulb" class="w-5 h-5 text-yellow-500" />
          Suggestions de reformulation
        </h3>
        <div class="space-y-4">
          <div
            v-for="(s, i) in analysis.analysis_details.suggestions"
            :key="i"
            class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
          >
            <p class="text-xs font-medium text-gray-400 uppercase mb-2">
              {{ s.reason }}
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div class="bg-red-50 dark:bg-red-950 rounded-lg p-3">
                <p class="text-xs font-medium text-red-600 mb-1">
                  Avant
                </p>
                <p class="text-sm text-red-800 dark:text-red-300">
                  {{ s.original }}
                </p>
              </div>
              <div class="bg-green-50 dark:bg-green-950 rounded-lg p-3">
                <div class="flex items-center justify-between mb-1">
                  <p class="text-xs font-medium text-green-600">
                    Après
                  </p>
                  <UButton
                    variant="ghost"
                    size="xs"
                    icon="i-lucide-copy"
                    color="success"
                    @click="copyToClipboard(s.improved)"
                  />
                </div>
                <p class="text-sm text-green-800 dark:text-green-300">
                  {{ s.improved }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Seniority match -->
      <UCard v-if="analysis.analysis_details?.seniority_match" class="mb-6">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <UIcon name="i-lucide-users" class="w-5 h-5 text-primary" />
          Correspondance de séniorité
        </h3>
        <div class="flex items-center gap-4">
          <div class="text-center">
            <p class="text-xs text-gray-400 mb-1">
              Votre profil
            </p>
            <UBadge color="neutral" size="lg" class="capitalize">
              {{ analysis.analysis_details.seniority_match.cv_level }}
            </UBadge>
          </div>
          <UIcon
            :name="analysis.analysis_details.seniority_match.match ? 'i-lucide-check' : 'i-lucide-x'"
            class="w-8 h-8 mx-2"
            :class="analysis.analysis_details.seniority_match.match ? 'text-green-500' : 'text-red-500'"
          />
          <div class="text-center">
            <p class="text-xs text-gray-400 mb-1">
              Poste requis
            </p>
            <UBadge color="neutral" size="lg" class="capitalize">
              {{ analysis.analysis_details.seniority_match.job_level }}
            </UBadge>
          </div>
          <p class="text-sm ml-4" :class="analysis.analysis_details.seniority_match.match ? 'text-green-600' : 'text-orange-500'">
            {{ analysis.analysis_details.seniority_match.match ? 'Niveaux compatibles' : 'Écart de niveau détecté' }}
          </p>
        </div>
      </UCard>

      <!-- CTA -->
      <div class="flex gap-3">
        <UButton to="/analyses/new" icon="i-lucide-plus">
          Nouvelle analyse
        </UButton>
        <UButton variant="outline" color="neutral" to="/analyses" icon="i-lucide-history">
          Historique
        </UButton>
      </div>
    </template>
  </div>
</template>
