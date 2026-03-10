<template>
  <div class="w-full max-w-sm rounded-xl border border-[#E2E8F0] bg-white p-5 shadow-[0_4px_12px_rgba(0,0,0,0.12)] select-none">
    <!-- Header -->
    <div class="flex items-start gap-3 mb-4">
      <div class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-[#1E3A5F] font-bold text-white text-base">
        JM
      </div>
      <div class="flex-1 min-w-0">
        <p class="font-semibold text-[#1A202C] text-sm">Jean-Paul Mbeki</p>
        <p class="text-[#718096] text-xs mt-0.5">jean.mbeki@email.com</p>
        <p class="text-[#718096] text-xs">Cotonou, Bénin</p>
      </div>
      <!-- Score -->
      <div class="flex flex-col items-center">
        <div class="flex h-12 w-12 items-center justify-center rounded-full border-4 border-[#38A169]">
          <span class="font-mono font-bold text-sm text-[#38A169]">82</span>
        </div>
        <span class="mt-1 text-[9px] text-[#718096] uppercase tracking-wider">Score</span>
      </div>
    </div>

    <!-- Skills -->
    <div class="mb-4 space-y-2">
      <p class="text-[10px] font-semibold uppercase tracking-wider text-[#718096] mb-2">Analyse IA</p>
      <ScoreBar label="Compétences" :value="88" color="#2E86AB" />
      <ScoreBar label="Expérience" :value="78" color="#2E86AB" />
      <ScoreBar label="Formation" :value="80" color="#2E86AB" />
      <ScoreBar label="Langues" :value="72" color="#2E86AB" />
    </div>

    <!-- Tags -->
    <div class="flex flex-wrap gap-1 mb-4">
      <span v-for="skill in ['React', 'TypeScript', 'Node.js', 'Docker', 'AWS']" :key="skill"
        class="rounded-md bg-[#F8F9FA] border border-[#E2E8F0] px-2 py-0.5 font-mono text-[10px] text-[#1A202C]">
        {{ skill }}
      </span>
    </div>

    <!-- Stage -->
    <div class="flex items-center justify-between rounded-md bg-[#F8F9FA] px-3 py-2">
      <span class="text-xs text-[#718096]">Étape actuelle</span>
      <span class="rounded-full bg-[#805AD5] px-2 py-0.5 text-[10px] font-semibold text-white">Entretien Tech</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const ScoreBar = defineComponent({
  props: {
    label: String,
    value: Number,
    color: String,
  },
  template: `
    <div class="flex items-center gap-2">
      <span class="w-20 flex-shrink-0 text-[10px] text-[#718096]">{{ label }}</span>
      <div class="flex-1 h-1.5 rounded-full bg-[#E2E8F0] overflow-hidden">
        <div class="h-full rounded-full transition-all" :style="{ width: value + '%', backgroundColor: color }" />
      </div>
      <span class="w-7 text-right font-mono text-[10px] font-bold" :style="{ color }">{{ value }}%</span>
    </div>
  `,
})
</script>
