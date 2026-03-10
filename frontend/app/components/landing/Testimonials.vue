<template>
  <section class="py-20 bg-[#F8F9FA]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">Témoignages</p>
        <h2 class="text-3xl font-bold text-[#1A202C] md:text-4xl">Ce que disent nos recruteurs</h2>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="(t, i) in testimonials"
          :key="t.name"
          :style="{ transform: `rotate(${rotations[i]}deg)` }"
          class="rounded-xl border border-[#E2E8F0] bg-white p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)] hover:rotate-0 transition-all duration-200"
        >
          <!-- Stars -->
          <div class="mb-4 flex gap-0.5">
            <svg v-for="n in 5" :key="n" class="h-4 w-4 text-[#D69E2E]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          </div>
          <p class="mb-5 text-sm italic leading-relaxed text-[#718096]">"{{ t.quote }}"</p>
          <div class="flex items-center gap-3">
            <div
              class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full font-semibold text-sm text-white"
              :style="{ backgroundColor: t.color }"
            >
              {{ t.initials }}
            </div>
            <div>
              <p class="text-sm font-semibold text-[#1A202C]">{{ t.name }}</p>
              <p class="text-xs text-[#718096]">{{ t.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const rotations = [-1, 0.5, -0.8]

const testimonials = [
  {
    quote: 'Avant ATS Platform, je passais 6 heures par offre à lire des CVs. Maintenant je reçois directement les 10 meilleurs profils scorés. C\'est un gain de temps incroyable.',
    name: 'xxxxxxx Marie Dupont',
    role: 'DRH · xxxxxxx, Paris',
    initials: 'MD',
    color: '#1E3A5F',
  },
  {
    quote: 'Le pipeline Kanban a transformé notre façon de travailler. Toute l\'équipe RH voit en temps réel où en est chaque candidat. Fini les emails de coordination.',
    name: 'xxxxxxx Thomas Garcia',
    role: 'Responsable Recrutement · xxxxxxx',
    initials: 'TG',
    color: '#2E86AB',
  },
  {
    quote: 'Le scoring IA est étonnamment précis. Sur nos derniers recrutements, les 3 candidats embauchés étaient tous dans le top 5 du classement automatique.',
    name: 'xxxxxxx Inès Kouassi',
    role: 'RH · xxxxxxx, Lyon',
    initials: 'IK',
    color: '#805AD5',
  },
]
</script>
