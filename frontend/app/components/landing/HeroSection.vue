<template>
  <section class="relative overflow-hidden bg-white pt-24 pb-16 md:pt-32 md:pb-24">
    <!-- Background gradient -->
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-br from-[#EBF4FA] via-white to-white" />

    <div class="relative mx-auto max-w-6xl px-6">
      <div class="grid items-center gap-12 lg:grid-cols-2">
        <!-- Left: text -->
        <div>
          <div class="mb-4 inline-flex items-center gap-2 rounded-full border border-[#E2E8F0] bg-white px-3 py-1.5 shadow-sm">
            <span class="h-2 w-2 rounded-full bg-[#38A169]" />
            <span class="text-xs font-medium text-[#718096]">Propulsé par IA · 100% gratuit pour démarrer</span>
          </div>

          <h1 class="mb-5 text-4xl font-bold leading-tight text-[#1A202C] md:text-5xl lg:text-[52px]">
            Recrutez plus vite,<br />
            <span class="text-[#2E86AB]">recrutez mieux.</span>
          </h1>

          <p class="mb-8 text-lg leading-relaxed text-[#718096] max-w-lg">
            ATS Platform centralise vos CVs, analyse chaque candidat avec l'IA en moins de 30 secondes
            et gère votre pipeline de recrutement en temps réel.
          </p>

          <div class="flex flex-wrap gap-3">
            <NuxtLink
              to="/register"
              class="inline-flex items-center gap-2 rounded-lg bg-[#1E3A5F] px-5 py-3 text-sm font-semibold text-white hover:bg-[#2E4E7A] transition-colors shadow-[0_1px_3px_rgba(0,0,0,0.08)]"
            >
              Commencer gratuitement
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </NuxtLink>
            <a
              href="#features"
              class="inline-flex items-center gap-2 rounded-lg border border-[#E2E8F0] bg-white px-5 py-3 text-sm font-semibold text-[#1E3A5F] hover:bg-[#F8F9FA] transition-colors"
            >
              Voir les fonctionnalités
            </a>
          </div>

          <p class="mt-4 text-xs text-[#718096]">
            Sans carte bancaire · Annulation à tout moment
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
