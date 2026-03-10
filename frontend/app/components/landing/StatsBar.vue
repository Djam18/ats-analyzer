<template>
  <section class="border-y border-[#E2E8F0] bg-[#F8F9FA] py-10">
    <div class="mx-auto max-w-6xl px-6">
      <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
        <div v-for="stat in stats" :key="stat.label" class="flex flex-col items-center text-center">
          <span class="font-mono text-4xl font-bold text-[#1E3A5F] md:text-5xl">{{ stat.value }}</span>
          <span class="mt-1 text-sm font-medium text-[#718096]">{{ stat.label }}</span>
          <span class="mt-1 text-xs text-[#38A169] font-semibold">{{ stat.sub }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const stats = [
  {
    value: '3×',
    label: 'Plus vite qu\'un recrutement manuel',
    sub: '23 jours ramenés à 8 en moyenne',
  },
  {
    value: '75%',
    label: 'Des CVs non qualifiés triés automatiquement',
    sub: 'Fini la lecture de CVs hors critères',
  },
  {
    value: '<30s',
    label: 'Par CV analysé par l\'IA',
    sub: 'Score calculé en temps réel',
  },
]
</script>
