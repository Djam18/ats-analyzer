<template>
  <section id="faq" class="py-20 bg-[#F8F9FA] dark:bg-[#1E293B]">
    <div class="mx-auto max-w-3xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">{{ $t('faq.label') }}</p>
        <h2 class="text-3xl font-bold text-[#1A202C] dark:text-white md:text-4xl">{{ $t('faq.title') }}</h2>
      </div>

      <div class="divide-y divide-[#E2E8F0] dark:divide-white/10 rounded-xl border border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-[#0F172A] overflow-hidden">
        <div v-for="(item, i) in faqs" :key="item.question">
          <button
            class="flex w-full items-center justify-between gap-4 px-6 py-5 text-left hover:bg-[#F8F9FA] dark:hover:bg-white/5 transition-colors"
            :aria-expanded="open === i"
            @click="open === i ? open = null : open = i"
          >
            <span class="font-semibold text-[#1A202C] dark:text-white text-sm">{{ item.question }}</span>
            <svg
              :class="['h-4 w-4 flex-shrink-0 text-[#718096] dark:text-white/40 transition-transform duration-200', open === i ? 'rotate-180' : '']"
              fill="none" stroke="currentColor" viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="open === i" role="region" class="px-6 pb-5">
            <p class="text-sm leading-relaxed text-[#718096] dark:text-white/60">{{ item.answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()
const open = ref<number | null>(0)

const faqs = computed(() => [
  { question: t('faq.q1'), answer: t('faq.a1') },
  { question: t('faq.q2'), answer: t('faq.a2') },
  { question: t('faq.q3'), answer: t('faq.a3') },
  { question: t('faq.q4'), answer: t('faq.a4') },
  { question: t('faq.q5'), answer: t('faq.a5') },
])
</script>
