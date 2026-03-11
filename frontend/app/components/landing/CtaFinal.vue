<template>
  <section class="py-20 bg-[#1E3A5F]">
    <div class="mx-auto max-w-3xl px-6 text-center">
      <h2 class="mb-4 text-3xl font-bold text-white md:text-4xl">
        {{ $t('cta.title') }}
      </h2>
      <p class="mb-8 text-lg text-white/70">
        {{ $t('cta.subtitle') }}
      </p>

      <div class="flex flex-wrap justify-center gap-3">
        <NuxtLink
          to="/register"
          class="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 text-sm font-bold text-[#1E3A5F] hover:bg-[#F8F9FA] transition-colors shadow-[0_1px_3px_rgba(0,0,0,0.12)]"
        >
          {{ $t('cta.primary') }}
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </NuxtLink>
        <a
          href="#features"
          class="inline-flex items-center gap-2 rounded-lg border border-white/30 px-6 py-3 text-sm font-semibold text-white hover:bg-white/10 transition-colors"
        >
          {{ $t('cta.secondary') }}
        </a>
      </div>

      <p class="mt-6 text-xs text-white/50">
        {{ $t('cta.footer_note') }}
      </p>
    </div>
  </section>
</template>
