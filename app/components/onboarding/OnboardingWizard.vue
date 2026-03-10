<script setup lang="ts">
const emit = defineEmits<{ complete: [] }>()

const currentStep = ref(0)
const totalSteps = 4

const uploadedCvId = ref<string | null>(null)

const steps = [
  { label: 'Découverte', icon: 'i-lucide-heart-handshake', description: 'Comment vous nous avez trouvé' },
  { label: 'Votre CV', icon: 'i-lucide-upload', description: 'Uploadez votre CV' },
  { label: 'L\'offre', icon: 'i-lucide-briefcase', description: 'Collez une offre d\'emploi' },
  { label: 'Analyse', icon: 'i-lucide-scan-text', description: 'Lancez votre première analyse' }
]

function handleReferralDone() {
  currentStep.value = 1
}

function handleCvUploaded(cvId: string) {
  uploadedCvId.value = cvId
  currentStep.value = 2
}

function handleJobDescriptionDone() {
  currentStep.value = 3
}

async function handleSkip() {
  const supabase = useSupabaseClient()
  const user = useSupabaseUser()
  if (!user.value) return
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  await (supabase as any)
    .from('profiles')
    .update({ onboarding_completed: true })
    .eq('id', user.value.id)
  await navigateTo('/dashboard')
}
</script>

<template>
  <div>
    <!-- Progress steps -->
    <div class="flex items-center justify-between mb-10">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="flex items-center"
        :class="index < steps.length - 1 ? 'flex-1' : ''"
      >
        <div class="flex flex-col items-center">
          <div
            class="w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all"
            :class="currentStep > index
              ? 'bg-primary border-primary text-white'
              : currentStep === index
                ? 'border-primary text-primary'
                : 'border-gray-300 text-gray-400'"
          >
            <UIcon v-if="currentStep > index" name="i-lucide-check" class="w-5 h-5" />
            <UIcon v-else :name="step.icon" class="w-5 h-5" />
          </div>
          <span class="text-xs mt-2 font-medium" :class="currentStep === index ? 'text-primary' : 'text-gray-400'">
            {{ step.label }}
          </span>
        </div>
        <div
          v-if="index < steps.length - 1"
          class="flex-1 h-0.5 mx-3 mb-5 transition-colors"
          :class="currentStep > index ? 'bg-primary' : 'bg-gray-200 dark:bg-gray-700'"
        />
      </div>
    </div>

    <!-- Step content -->
    <UCard>
      <OnboardingStepReferralSource
        v-if="currentStep === 0"
        @done="handleReferralDone"
      />
      <OnboardingStepUploadCv
        v-else-if="currentStep === 1"
        @uploaded="handleCvUploaded"
      />
      <OnboardingStepJobDescription
        v-else-if="currentStep === 2"
        :cv-id="uploadedCvId!"
        @done="handleJobDescriptionDone"
      />
      <OnboardingStepLaunchAnalysis
        v-else-if="currentStep === 3"
        :cv-id="uploadedCvId!"
        @complete="emit('complete')"
      />
    </UCard>

    <!-- Skip button -->
    <div class="text-center mt-6">
      <UButton variant="ghost" color="neutral" size="sm" @click="handleSkip">
        Passer l'introduction
      </UButton>
    </div>
  </div>
</template>
