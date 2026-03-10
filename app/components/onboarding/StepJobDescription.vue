<script setup lang="ts">
defineProps<{ cvId: string }>()
const emit = defineEmits<{ done: [] }>()

const jobTitle = ref('')
const companyName = ref('')
const jobDescription = ref('')

const charCount = computed(() => jobDescription.value.length)
const isValid = computed(() =>
  jobTitle.value.trim().length > 0
  && charCount.value >= 100
  && charCount.value <= 10000
)
</script>

<template>
  <div class="py-4">
    <div class="text-center mb-6">
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
        Collez une offre d'emploi
      </h2>
      <p class="text-gray-500 dark:text-gray-400 text-sm">
        Copiez-collez le texte complet de l'offre pour un meilleur score
      </p>
    </div>

    <div class="space-y-4">
      <UFormField label="Titre du poste *" required>
        <UInput
          v-model="jobTitle"
          placeholder="ex: Développeur Full Stack"
          class="w-full"
        />
      </UFormField>

      <UFormField label="Entreprise">
        <UInput
          v-model="companyName"
          placeholder="ex: Google"
          class="w-full"
        />
      </UFormField>

      <UFormField label="Description du poste *" required>
        <UTextarea
          v-model="jobDescription"
          placeholder="Collez ici le texte complet de l'offre d'emploi..."
          :rows="8"
          class="w-full"
        />
        <template #help>
          <span :class="charCount < 100 ? 'text-error-500' : 'text-gray-400'">
            {{ charCount.toLocaleString() }} / 10 000 caractères
            <span v-if="charCount < 100"> (minimum 100)</span>
          </span>
        </template>
      </UFormField>
    </div>

    <div class="mt-6 flex justify-end">
      <UButton :disabled="!isValid" @click="emit('done')">
        Continuer
        <UIcon name="i-lucide-arrow-right" class="ml-2 w-4 h-4" />
      </UButton>
    </div>
  </div>
</template>
