<template>
  <section class="border-y border-[#E2E8F0] dark:border-white/10 bg-[#F8F9FA] dark:bg-[#1E293B] py-10">
    <div class="mx-auto max-w-6xl px-6">
      <div class="grid grid-cols-1 gap-8 md:grid-cols-3">
        <div v-for="stat in stats" :key="stat.label" class="flex flex-col items-center text-center">
          <span class="font-mono text-4xl font-bold text-[#1E3A5F] dark:text-secondary md:text-5xl">{{ stat.value }}</span>
          <span class="mt-1 text-sm font-medium text-[#718096] dark:text-white/60">{{ stat.label }}</span>
          <span class="mt-1 text-xs text-[#38A169] font-semibold">{{ stat.sub }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t } = useI18n()

const stats = computed(() => [
  { value: t('stats.item1_value'), label: t('stats.item1_label'), sub: t('stats.item1_sub') },
  { value: t('stats.item2_value'), label: t('stats.item2_label'), sub: t('stats.item2_sub') },
  { value: t('stats.item3_value'), label: t('stats.item3_label'), sub: t('stats.item3_sub') },
])
</script>
