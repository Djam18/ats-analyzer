<template>
  <div class="min-h-screen bg-[#F8F9FA] dark:bg-[#0F172A] flex flex-col items-center justify-center px-6 py-16">
    <div class="text-center max-w-lg">
      <div class="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-[#EBF4FA] dark:bg-[#1E3A5F]/30">
        <svg class="h-8 w-8 text-[#2E86AB]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>

      <h1 class="mb-3 text-3xl font-bold text-[#1A202C] dark:text-white">
        {{ $t('docs.title') }}
      </h1>
      <p class="mb-2 text-lg font-medium text-[#2E86AB]">{{ $t('docs.coming_soon') }}</p>
      <p class="mb-8 text-[#718096] dark:text-white/60">{{ $t('docs.subtitle') }}</p>

      <div class="flex flex-wrap justify-center gap-3">
        <NuxtLink
          to="/#faq"
          class="rounded-lg bg-[#1E3A5F] dark:bg-[#2E86AB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#2E4E7A] dark:hover:bg-[#3A9BC0] transition-colors"
        >
          {{ $t('docs.faq_link') }}
        </NuxtLink>
        <a
          href="mailto:bonjour@ats-platform.fr"
          class="rounded-lg border border-[#E2E8F0] dark:border-white/10 px-5 py-2.5 text-sm font-semibold text-[#1E3A5F] dark:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5 transition-colors"
        >
          {{ $t('docs.contact_link') }}
        </a>
      </div>

      <NuxtLink to="/" class="mt-8 inline-block text-sm text-[#718096] hover:text-[#1E3A5F] dark:hover:text-white transition-colors">
        {{ $t('docs.back_home') }}
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
useHead({ title: () => t('docs.page_title') })
</script>
