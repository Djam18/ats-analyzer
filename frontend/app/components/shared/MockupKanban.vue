<template>
  <div class="w-full rounded-xl border border-[#E2E8F0] bg-[#F8F9FA] p-4 shadow-[0_4px_12px_rgba(0,0,0,0.12)] select-none">
    <!-- Header -->
    <div class="mb-3 flex items-center gap-2">
      <div class="h-3 w-3 rounded-full bg-[#E53E3E]" />
      <div class="h-3 w-3 rounded-full bg-[#D69E2E]" />
      <div class="h-3 w-3 rounded-full bg-[#38A169]" />
      <span class="ml-2 text-xs font-medium text-[#718096]">Pipeline — Dev React Senior</span>
    </div>

    <!-- Columns -->
    <div class="grid grid-cols-4 gap-2">
      <!-- Reçu -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-1 mb-1">
          <div class="h-2 w-2 rounded-full bg-[#718096]" />
          <span class="text-[10px] font-semibold uppercase tracking-wider text-[#718096]">Reçus</span>
          <span class="ml-auto text-[10px] font-bold text-[#718096]">45</span>
        </div>
        <KanbanCard name="S. Agossa" score="71" color="#718096" />
        <KanbanCard name="M. Dossou" score="55" color="#718096" />
        <KanbanCard name="P. Kone" score="68" color="#718096" />
      </div>

      <!-- Présélection -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-1 mb-1">
          <div class="h-2 w-2 rounded-full bg-[#3182CE]" />
          <span class="text-[10px] font-semibold uppercase tracking-wider text-[#3182CE]">Présél.</span>
          <span class="ml-auto text-[10px] font-bold text-[#3182CE]">12</span>
        </div>
        <KanbanCard name="A. Kounde" score="79" color="#3182CE" />
        <KanbanCard name="L. Brou" score="76" color="#3182CE" />
      </div>

      <!-- Entretien -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-1 mb-1">
          <div class="h-2 w-2 rounded-full bg-[#805AD5]" />
          <span class="text-[10px] font-semibold uppercase tracking-wider text-[#805AD5]">Entretien</span>
          <span class="ml-auto text-[10px] font-bold text-[#805AD5]">8</span>
        </div>
        <KanbanCard name="J.P. Mbeki" score="82" color="#805AD5" highlight />
        <KanbanCard name="F. Touré" score="88" color="#805AD5" />
      </div>

      <!-- Offre -->
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-1 mb-1">
          <div class="h-2 w-2 rounded-full bg-[#38A169]" />
          <span class="text-[10px] font-semibold uppercase tracking-wider text-[#38A169]">Offre</span>
          <span class="ml-auto text-[10px] font-bold text-[#38A169]">3</span>
        </div>
        <KanbanCard name="C. Mensah" score="91" color="#38A169" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const KanbanCard = defineComponent({
  props: {
    name: String,
    score: String,
    color: String,
    highlight: Boolean,
  },
  template: `
    <div
      :style="{ borderLeftColor: color }"
      :class="[
        'rounded-md border border-[#E2E8F0] border-l-2 bg-white p-2 shadow-[0_1px_3px_rgba(0,0,0,0.08)]',
        highlight ? 'ring-1 ring-[#2E86AB]' : ''
      ]"
    >
      <p class="text-[10px] font-semibold text-[#1A202C] truncate">{{ name }}</p>
      <p class="text-[10px] font-mono font-bold" :style="{ color }">{{ score }}/100</p>
    </div>
  `,
})
</script>
