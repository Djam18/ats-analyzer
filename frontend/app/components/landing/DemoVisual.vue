<template>
  <section class="py-20 bg-white">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">Aperçu produit</p>
        <h2 class="text-3xl font-bold text-[#1A202C] md:text-4xl">Chaque candidat, en un coup d'œil</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096]">
          L'IA extrait et structure toutes les informations du CV. Vous voyez immédiatement si le profil correspond à votre offre.
        </p>
      </div>

      <div class="flex justify-center">
        <div class="relative">
          <!-- Glow effect -->
          <div class="absolute -inset-4 rounded-2xl bg-[#2E86AB]/10 blur-xl" />
          <div class="relative -rotate-1 hover:rotate-0 transition-transform duration-300">
            <SharedMockupProfile />
          </div>
        </div>
      </div>

      <!-- Feature pills below -->
      <div class="mt-12 flex flex-wrap justify-center gap-3">
        <span v-for="pill in pills" :key="pill" class="rounded-full border border-[#E2E8F0] bg-[#F8F9FA] px-4 py-1.5 text-sm font-medium text-[#718096]">
          {{ pill }}
        </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const pills = [
  'Score de matching 0–100',
  'Compétences détectées automatiquement',
  'Années d\'expérience extraites',
  'Niveau de formation analysé',
  'Langues identifiées',
  'CV original téléchargeable',
]
</script>
