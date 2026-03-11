<template>
  <div class="min-h-screen bg-[#F8F9FA] dark:bg-[#0F172A]">
    <div class="mx-auto max-w-3xl px-6 py-16">
      <NuxtLink to="/" class="mb-8 inline-block text-sm text-[#2E86AB] hover:underline">
        {{ $t('legal_mentions.back_home') }}
      </NuxtLink>

      <h1 class="mb-10 text-3xl font-bold text-[#1A202C] dark:text-white">
        {{ $t('legal_mentions.title') }}
      </h1>

      <div class="space-y-8">
        <section v-for="section in sections" :key="section.title">
          <h2 class="mb-3 text-lg font-semibold text-[#1A202C] dark:text-white">
            {{ $t(section.title) }}
          </h2>
          <p class="text-[#4A5568] dark:text-white/70 leading-relaxed">
            {{ $t(section.body) }}
          </p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({ title: () => t('legal_mentions.page_title') })

const sections = [
  { title: 'legal_mentions.editor_title', body: 'legal_mentions.editor_body' },
  { title: 'legal_mentions.host_title', body: 'legal_mentions.host_body' },
  { title: 'legal_mentions.contact_title', body: 'legal_mentions.contact_body' },
  { title: 'legal_mentions.ip_title', body: 'legal_mentions.ip_body' },
]
</script>
