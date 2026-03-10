<script setup lang="ts">
import type { CV } from '~/composables/useCV'

definePageMeta({ middleware: ['auth', 'onboarding'] })

const { t } = useI18n()
const { fetchCVs } = useCV()
const { createAnalysis } = useAnalysis()
const { quota, fetchQuota } = useQuota()

const cvs = ref<CV[]>([])
const selectedCvId = ref<string | null>(null)
const jobTitle = ref('')
const companyName = ref('')
const jobDescription = ref('')
const loading = ref(false)
const loadingCvs = ref(true)

const charCount = computed(() => jobDescription.value.length)
const isValid = computed(() =>
  selectedCvId.value
  && jobTitle.value.trim().length >= 2
  && charCount.value >= 100
  && charCount.value <= 10000
)

onMounted(async () => {
  await fetchQuota()
  cvs.value = await fetchCVs()
  loadingCvs.value = false
})

async function handleSubmit() {
  if (!isValid.value || !selectedCvId.value) return
  loading.value = true

  const result = await createAnalysis({
    cv_id: selectedCvId.value,
    job_title: jobTitle.value.trim(),
    company_name: companyName.value.trim() || undefined,
    job_description: jobDescription.value.trim()
  })

  loading.value = false

  if (result) {
    await navigateTo(`/analyses/${result.id}`)
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ t('analysis.new.title') }}
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        {{ t('analysis.new.selectCv') }}
      </p>
    </div>

    <UAlert
      v-if="quota && !quota.allowed"
      icon="i-lucide-alert-triangle"
      color="warning"
      variant="soft"
      :title="t('analysis.new.quotaExhausted')"
      class="mb-6"
    >
      <template #actions>
        <UButton to="/pricing" size="sm" color="warning">
          {{ t('analysis.new.upgrade') }}
        </UButton>
      </template>
    </UAlert>

    <form class="space-y-6" @submit.prevent="handleSubmit">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 rounded-full bg-primary text-white text-xs font-bold flex items-center justify-center">
              1
            </div>
            <h2 class="font-semibold text-gray-900 dark:text-white">
              {{ t('analysis.new.selectCv') }}
            </h2>
          </div>
        </template>

        <div v-if="loadingCvs" class="space-y-3">
          <div v-for="i in 2" :key="i" class="h-16 bg-gray-100 dark:bg-gray-800 rounded-lg animate-pulse" />
        </div>

        <SharedEmptyState
          v-else-if="cvs.length === 0"
          icon="i-lucide-file-text"
          :title="t('cv.empty.title')"
          :description="t('cv.empty.subtitle')"
          :action-label="t('cv.empty.cta')"
          action-to="/cvs"
        />

        <div v-else class="space-y-3">
          <CvCard
            v-for="cv in cvs"
            :key="cv.id"
            :cv="cv"
            :selected="cv.id === selectedCvId"
            @select="selectedCvId = $event"
          />
        </div>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <div class="w-6 h-6 rounded-full bg-primary text-white text-xs font-bold flex items-center justify-center">
              2
            </div>
            <h2 class="font-semibold text-gray-900 dark:text-white">
              {{ t('analysis.new.jobDescription') }}
            </h2>
          </div>
        </template>

        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <UFormField :label="`${t('analysis.new.jobTitle')} *`" required>
              <UInput
                v-model="jobTitle"
                placeholder="ex: Développeur Full Stack"
                class="w-full"
              />
            </UFormField>
            <UFormField :label="t('analysis.new.company')">
              <UInput
                v-model="companyName"
                placeholder="ex: Google"
                class="w-full"
              />
            </UFormField>
          </div>

          <UFormField :label="`${t('analysis.new.jobDescription')} *`" required>
            <UTextarea
              v-model="jobDescription"
              :placeholder="t('analysis.new.jobDescriptionHint')"
              :rows="10"
              class="w-full"
            />
            <template #help>
              <span :class="charCount < 100 ? 'text-red-500' : 'text-gray-400'">
                {{ charCount.toLocaleString() }} / 10 000
                <span v-if="charCount < 100"> — minimum 100</span>
              </span>
            </template>
          </UFormField>
        </div>
      </UCard>

      <UButton
        type="submit"
        size="lg"
        class="w-full"
        icon="i-lucide-scan-text"
        :loading="loading"
        :disabled="!isValid || (quota !== null && !quota.allowed)"
      >
        {{ loading ? t('common.loading') : t('analysis.new.submit') }}
      </UButton>
    </form>
  </div>
</template>
