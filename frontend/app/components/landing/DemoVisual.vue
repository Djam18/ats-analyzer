<template>
  <section class="py-20 bg-white dark:bg-[#0F172A]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">{{ $t('demo.label') }}</p>
        <h2 class="text-3xl font-bold text-[#1A202C] dark:text-white md:text-4xl">{{ $t('demo.title') }}</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096] dark:text-white/60">
          {{ $t('demo.subtitle') }}
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
        <span
          v-for="pill in pills"
          :key="pill"
          class="rounded-full border border-[#E2E8F0] dark:border-white/10 bg-[#F8F9FA] dark:bg-white/5 px-4 py-1.5 text-sm font-medium text-[#718096] dark:text-white/60"
        >
          {{ pill }}
        </span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

const pills = computed(() => [
  t('demo.pill1'),
  t('demo.pill2'),
  t('demo.pill3'),
  t('demo.pill4'),
  t('demo.pill5'),
  t('demo.pill6'),
])
</script>
