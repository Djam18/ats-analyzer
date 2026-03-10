<template>
  <section class="py-20 bg-white">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">Le problème</p>
        <h2 class="text-3xl font-bold text-[#1A202C] md:text-4xl">Vos défis quotidiens en recrutement</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096]">
          Les équipes RH passent plus de temps à trier et suivre les CVs qu'à évaluer les vrais talents.
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="pain in pains"
          :key="pain.title"
          :style="{ borderLeftColor: pain.color }"
          class="rounded-xl border border-[#E2E8F0] border-l-4 bg-white p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)] transition-shadow"
        >
          <div
            class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl"
            :style="{ backgroundColor: pain.color + '18' }"
          >
            <component :is="pain.icon" class="h-5 w-5" :style="{ color: pain.color }" />
          </div>
          <h3 class="mb-2 font-semibold text-[#1A202C]">{{ pain.title }}</h3>
          <p class="text-sm leading-relaxed text-[#718096]">{{ pain.desc }}</p>
          <p class="mt-3 text-xs font-semibold" :style="{ color: pain.color }">{{ pain.stat }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Clock, FolderOpen, BarChart2 } from 'lucide-vue-next'

const pains = [
  {
    icon: Clock,
    color: '#E53E3E',
    title: 'Tri manuel épuisant',
    desc: 'Vous passez des heures à lire des CVs qui ne correspondent pas, avant même de savoir si le profil est qualifié.',
    stat: '~6h de tri par offre pour 250 candidatures',
  },
  {
    icon: FolderOpen,
    color: '#D69E2E',
    title: 'Données éparpillées',
    desc: 'CVs dans les emails, Google Drive, Slack, fichiers Excel… Aucune traçabilité, aucune vision d\'ensemble.',
    stat: '0% de traçabilité sans outil centralisé',
  },
  {
    icon: BarChart2,
    color: '#3182CE',
    title: 'Zéro reporting',
    desc: 'Impossible de mesurer le coût d\'un recrutement, le délai par étape, ou le taux de conversion de votre pipeline.',
    stat: '4 500 € de coût moyen par recrutement en PME',
  },
]
</script>
