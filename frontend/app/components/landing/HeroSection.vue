<template>
  <section class="relative overflow-hidden bg-white dark:bg-[#0F172A] pt-24 pb-16 md:pt-32 md:pb-24">
    <!-- Background gradient -->
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-br from-[#EBF4FA] via-white to-white dark:from-[#1E3A5F]/20 dark:via-[#0F172A] dark:to-[#0F172A]" />

    <div class="relative mx-auto max-w-6xl px-6">
      <div class="grid items-center gap-12 lg:grid-cols-2">
        <!-- Left: text -->
        <div>
          <div class="mb-4 inline-flex items-center gap-2 rounded-full border border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-white/5 px-3 py-1.5 shadow-sm">
            <span class="h-2 w-2 rounded-full bg-[#38A169]" />
            <span class="text-xs font-medium text-[#718096] dark:text-white/60">{{ $t('hero.badge') }}</span>
          </div>

          <h1 class="mb-5 text-4xl font-bold leading-tight text-[#1A202C] dark:text-white md:text-5xl lg:text-[52px]">
            {{ $t('hero.title_line1') }}<br />
            <span class="text-[#2E86AB]">{{ $t('hero.title_line2') }}</span>
          </h1>

          <p class="mb-8 text-lg leading-relaxed text-[#718096] dark:text-white/60 max-w-lg">
            {{ $t('hero.description') }}
          </p>

          <div class="flex flex-wrap gap-3">
            <NuxtLink
              to="/register"
              class="inline-flex items-center gap-2 rounded-lg bg-[#1E3A5F] dark:bg-[#2E86AB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#2E4E7A] dark:hover:bg-[#3A9BC0] transition-colors shadow-[0_1px_3px_rgba(0,0,0,0.08)]"
            >
              {{ $t('hero.cta_primary') }}
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
            <a
              href="#features"
              class="inline-flex items-center gap-2 rounded-lg border border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-white/5 px-5 py-3 text-sm font-semibold text-[#1E3A5F] dark:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/10 transition-colors"
            >
              {{ $t('hero.cta_secondary') }}
            </a>
          </div>

          <p class="mt-4 text-xs text-[#718096] dark:text-white/40">
            {{ $t('hero.no_card') }}
          </p>
        </div>

        <!-- Right: mockup -->
        <div class="flex justify-center lg:justify-end">
          <div class="w-full max-w-lg">
            <SharedMockupKanban />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
