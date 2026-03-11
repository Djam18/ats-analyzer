<template>
  <section class="py-20 bg-white dark:bg-[#0F172A]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">{{ $t('pain.label') }}</p>
        <h2 class="text-3xl font-bold text-[#1A202C] dark:text-white md:text-4xl">{{ $t('pain.title') }}</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096] dark:text-white/60">
          {{ $t('pain.subtitle') }}
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="pain in pains"
          :key="pain.title"
          :style="{ borderLeftColor: pain.color }"
          class="rounded-xl border border-[#E2E8F0] dark:border-white/10 border-l-4 bg-white dark:bg-[#1E293B] p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)] hover:shadow-[0_4px_12px_rgba(0,0,0,0.12)] transition-shadow"
        >
          <div
            class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl"
            :style="{ backgroundColor: pain.color + '18' }"
          >
            <component :is="pain.icon" class="h-5 w-5" :style="{ color: pain.color }" />
          </div>
          <h3 class="mb-2 font-semibold text-[#1A202C] dark:text-white">{{ pain.title }}</h3>
          <p class="text-sm leading-relaxed text-[#718096] dark:text-white/60">{{ pain.desc }}</p>
          <p class="mt-3 text-xs font-semibold" :style="{ color: pain.color }">{{ pain.stat }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Clock, FolderOpen, BarChart2 } from 'lucide-vue-next'

const { t } = useI18n()

const pains = computed(() => [
  {
    icon: Clock,
    color: '#E53E3E',
    title: t('pain.item1_title'),
    desc: t('pain.item1_desc'),
    stat: t('pain.item1_stat'),
  },
  {
    icon: FolderOpen,
    color: '#D69E2E',
    title: t('pain.item2_title'),
    desc: t('pain.item2_desc'),
    stat: t('pain.item2_stat'),
  },
  {
    icon: BarChart2,
    color: '#3182CE',
    title: t('pain.item3_title'),
    desc: t('pain.item3_desc'),
    stat: t('pain.item3_stat'),
  },
])
</script>
