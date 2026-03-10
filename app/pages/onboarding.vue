<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
  layout: 'onboarding'
})
</script>

<template>
  <div>
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Bienvenue sur ATS Analyzer
      </h1>
      <p class="text-gray-500 dark:text-gray-400">
        Configurons votre premier projet en 3 étapes
      </p>
    </div>

    <OnboardingWizard />
  </div>
</template>
