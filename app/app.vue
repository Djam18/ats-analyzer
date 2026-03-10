<script setup lang="ts">
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'fr'
  }
})

useSeoMeta({
  title: 'ATS Analyzer — Optimisez votre CV pour les recruteurs',
  description: 'Analysez la compatibilité de votre CV avec une offre d\'emploi et obtenez un score ATS avec des recommandations concrètes.',
  ogTitle: 'ATS Analyzer',
  ogDescription: 'Analysez la compatibilité de votre CV avec une offre d\'emploi.'
})
</script>

<template>
  <UApp>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
