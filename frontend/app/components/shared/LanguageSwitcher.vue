<template>
  <div class="relative" ref="container">
    <button
      @click="open = !open"
      class="flex h-9 items-center gap-1.5 rounded-lg border border-[#E2E8F0] dark:border-white/10 px-2.5 text-xs font-medium text-[#718096] dark:text-white/60 hover:text-[#1E3A5F] dark:hover:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5 transition-colors"
      :aria-label="`Language: ${currentLocale?.name}`"
      :aria-expanded="open"
    >
      <span>{{ currentLocale?.code.toUpperCase() }}</span>
      <svg
        :class="['h-3 w-3 transition-transform duration-150', open ? 'rotate-180' : '']"
        fill="none" stroke="currentColor" viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <div
      v-if="open"
      class="absolute right-0 top-full mt-1.5 z-50 min-w-[130px] rounded-lg border border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-[#1E293B] shadow-[0_4px_12px_rgba(0,0,0,0.12)] overflow-hidden"
    >
      <button
        v-for="locale in locales"
        :key="locale.code"
        @click="switchLocale(locale.code)"
        :class="[
          'flex w-full items-center gap-2.5 px-3 py-2 text-left text-xs transition-colors',
          locale.code === currentCode
            ? 'bg-[#F0F7FB] dark:bg-[#1E3A5F]/30 text-[#1E3A5F] dark:text-[#2E86AB] font-semibold'
            : 'text-[#718096] dark:text-white/60 hover:bg-[#F8F9FA] dark:hover:bg-white/5 hover:text-[#1A202C] dark:hover:text-white',
        ]"
      >
        <span class="font-mono text-[10px] font-bold opacity-60">{{ locale.code.toUpperCase() }}</span>
        <span>{{ locale.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const { locale, locales, setLocale } = useI18n()
const open = ref(false)
const container = ref<HTMLElement | null>(null)

const currentCode = computed(() => locale.value)
const currentLocale = computed(() =>
  (locales.value as Array<{ code: string; name: string }>).find(l => l.code === currentCode.value)
)

async function switchLocale(code: string) {
  await setLocale(code)
  open.value = false
}

onMounted(() => {
  const handler = (e: MouseEvent) => {
    if (container.value && !container.value.contains(e.target as Node)) {
      open.value = false
    }
  }
  document.addEventListener('mousedown', handler)
  onBeforeUnmount(() => document.removeEventListener('mousedown', handler))
})
</script>
