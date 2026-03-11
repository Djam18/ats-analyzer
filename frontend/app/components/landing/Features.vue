<template>
  <section id="features" class="py-20 bg-[#F8F9FA] dark:bg-[#1E293B]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-16 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">{{ $t('features.label') }}</p>
        <h2 class="text-3xl font-bold text-[#1A202C] dark:text-white md:text-4xl">{{ $t('features.title') }}</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096] dark:text-white/60">
          {{ $t('features.subtitle') }}
        </p>
      </div>

      <div class="flex flex-col gap-16">
        <div
          v-for="(feature, i) in features"
          :key="feature.title"
          :class="[
            'grid items-center gap-10 lg:grid-cols-2',
            i % 2 === 1 ? 'lg:flex lg:flex-row-reverse' : '',
          ]"
        >
          <!-- Text -->
          <div :class="i % 2 === 1 ? 'lg:pl-10' : 'lg:pr-10'">
            <div
              class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl"
              :style="{ backgroundColor: feature.color + '18' }"
            >
              <component :is="feature.icon" class="h-5 w-5" :style="{ color: feature.color }" />
            </div>
            <h3 class="mb-3 text-xl font-bold text-[#1A202C] dark:text-white">{{ feature.title }}</h3>
            <p class="mb-5 text-[#718096] dark:text-white/60">{{ feature.desc }}</p>
            <ul class="space-y-2.5">
              <li v-for="point in feature.points" :key="point" class="flex items-start gap-2.5">
                <svg class="mt-0.5 h-4 w-4 flex-shrink-0 text-[#38A169]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
                <span class="text-sm text-[#1A202C] dark:text-white/80">{{ point }}</span>
              </li>
            </ul>
          </div>

          <!-- Visual -->
          <div class="flex justify-center">
            <div
              class="flex h-56 w-full max-w-md items-center justify-center rounded-2xl border border-[#E2E8F0] dark:border-white/10"
              :style="{ background: `linear-gradient(135deg, ${feature.color}12, ${feature.color}06)` }"
            >
              <component :is="feature.icon" class="h-20 w-20 opacity-20" :style="{ color: feature.color }" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Briefcase, Upload, Star, LayoutDashboard, Mail, BarChart2 } from 'lucide-vue-next'

const { t } = useI18n()

const features = computed(() => [
  {
    icon: Briefcase,
    color: '#1E3A5F',
    title: t('features.f1_title'),
    desc: t('features.f1_desc'),
    points: [t('features.f1_p1'), t('features.f1_p2'), t('features.f1_p3')],
  },
  {
    icon: Upload,
    color: '#2E86AB',
    title: t('features.f2_title'),
    desc: t('features.f2_desc'),
    points: [t('features.f2_p1'), t('features.f2_p2'), t('features.f2_p3')],
  },
  {
    icon: Star,
    color: '#D69E2E',
    title: t('features.f3_title'),
    desc: t('features.f3_desc'),
    points: [t('features.f3_p1'), t('features.f3_p2'), t('features.f3_p3')],
  },
  {
    icon: LayoutDashboard,
    color: '#805AD5',
    title: t('features.f4_title'),
    desc: t('features.f4_desc'),
    points: [t('features.f4_p1'), t('features.f4_p2'), t('features.f4_p3')],
  },
  {
    icon: Mail,
    color: '#38A169',
    title: t('features.f5_title'),
    desc: t('features.f5_desc'),
    points: [t('features.f5_p1'), t('features.f5_p2'), t('features.f5_p3')],
  },
  {
    icon: BarChart2,
    color: '#E53E3E',
    title: t('features.f6_title'),
    desc: t('features.f6_desc'),
    points: [t('features.f6_p1'), t('features.f6_p2'), t('features.f6_p3')],
  },
])
</script>
