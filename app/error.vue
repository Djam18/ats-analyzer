<script setup lang="ts">
const props = defineProps<{
  error: { statusCode: number, message: string }
}>()

const handleError = () => clearError({ redirect: '/' })

const title = computed(() => {
  if (props.error.statusCode === 404) return 'Page introuvable'
  if (props.error.statusCode === 403) return 'Accès refusé'
  return 'Une erreur est survenue'
})

const description = computed(() => {
  if (props.error.statusCode === 404) return 'La page que vous cherchez n\'existe pas ou a été déplacée.'
  if (props.error.statusCode === 403) return 'Vous n\'avez pas les droits pour accéder à cette ressource.'
  return 'Quelque chose s\'est mal passé. Réessayez ou revenez à l\'accueil.'
})
</script>

<template>
  <UApp>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center p-4">
      <div class="text-center max-w-md">
        <div class="text-6xl font-bold text-primary mb-4">
          {{ error.statusCode }}
        </div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
          {{ title }}
        </h1>
        <p class="text-gray-500 dark:text-gray-400 mb-8">
          {{ description }}
        </p>
        <UButton icon="i-lucide-home" @click="handleError">
          Retour à l'accueil
        </UButton>
      </div>
    </div>
  </UApp>
</template>
