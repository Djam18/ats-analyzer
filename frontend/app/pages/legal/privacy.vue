<template>
  <div class="min-h-screen bg-[#F8F9FA] dark:bg-[#0F172A]">
    <div class="mx-auto max-w-3xl px-6 py-16">
      <NuxtLink to="/" class="mb-8 inline-block text-sm text-[#2E86AB] hover:underline">
        {{ $t('legal_privacy.back_home') }}
      </NuxtLink>

      <h1 class="mb-2 text-3xl font-bold text-[#1A202C] dark:text-white">
        {{ $t('legal_privacy.title') }}
      </h1>
      <p class="mb-10 text-sm text-[#718096] dark:text-white/50">{{ $t('legal_privacy.last_updated') }}</p>

      <p class="mb-8 text-[#4A5568] dark:text-white/70 leading-relaxed">{{ $t('legal_privacy.intro') }}</p>

      <div class="space-y-8">
        <section v-for="n in [1,2,3,4,5]" :key="n">
          <h2 class="mb-3 text-lg font-semibold text-[#1A202C] dark:text-white">
            {{ $t(`legal_privacy.s${n}_title`) }}
          </h2>
          <p class="text-[#4A5568] dark:text-white/70 leading-relaxed">
            {{ $t(`legal_privacy.s${n}_body`) }}
          </p>
        </section>
      </div>

      <p class="mt-12 text-sm text-[#718096] dark:text-white/50 border-t border-[#E2E8F0] dark:border-white/10 pt-6">
        {{ $t('legal_privacy.contact') }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
useHead({ title: () => t('legal_privacy.page_title') })
</script>
