<script setup lang="ts">
const { t } = useI18n()
const { isDark, toggle } = useDarkMode()

const scrolled = ref(false)
const mobileOpen = ref(false)

const navLinks = computed(() => [
  { label: t('nav.features'), href: '#features' },
  { label: t('nav.pricing'), href: '#pricing' },
  { label: t('nav.faq'), href: '#faq' },
])

onMounted(() => {
  const handler = () => { scrolled.value = window.scrollY > 10 }
  window.addEventListener('scroll', handler, { passive: true })
  onBeforeUnmount(() => window.removeEventListener('scroll', handler))
})
</script>

<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-200',
      scrolled
        ? 'bg-white dark:bg-[#0F172A] border-b border-[#E2E8F0] dark:border-white/10 shadow-[0_1px_3px_rgba(0,0,0,0.08)]'
        : 'bg-white/90 dark:bg-[#0F172A]/90 backdrop-blur-sm',
    ]"
  >
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
      <SharedLogo size="md" />

      <nav class="hidden md:flex items-center gap-6">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="text-sm font-medium text-[#718096] dark:text-white/60 hover:text-[#1E3A5F] dark:hover:text-white transition-colors"
        >
          {{ link.label }}
        </a>
      </nav>

      <div class="hidden md:flex items-center gap-2">
        <!-- Language switcher -->
        <SharedLanguageSwitcher />

        <!-- Dark mode toggle -->
        <button
          @click="toggle"
          class="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E2E8F0] dark:border-white/10 text-[#718096] dark:text-white/60 hover:text-[#1E3A5F] dark:hover:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5 transition-colors"
          :aria-label="isDark ? $t('nav.aria_light_mode') : $t('nav.aria_dark_mode')"
        >
          <svg v-if="isDark" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
          </svg>
          <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

        <NuxtLink
          to="/login"
          class="text-sm font-medium text-[#1E3A5F] dark:text-white/80 hover:text-[#2E86AB] dark:hover:text-white transition-colors px-3 py-2"
        >
          {{ $t('nav.login') }}
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="rounded-lg bg-[#1E3A5F] dark:bg-[#2E86AB] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2E4E7A] dark:hover:bg-[#3A9BC0] transition-colors"
        >
          {{ $t('nav.start_free') }}
        </NuxtLink>
      </div>

      <!-- Mobile: dark toggle + hamburger -->
      <div class="md:hidden flex items-center gap-2">
        <SharedLanguageSwitcher />
        <button
          @click="toggle"
          class="flex h-9 w-9 items-center justify-center rounded-lg border border-[#E2E8F0] dark:border-white/10 text-[#718096] dark:text-white/60"
          :aria-label="isDark ? $t('nav.aria_light_mode_short') : $t('nav.aria_dark_mode_short')"
        >
          <svg v-if="isDark" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m12.728 0l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
          </svg>
          <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>
        <button
          class="p-2 rounded-md text-[#718096] dark:text-white/60 hover:text-[#1E3A5F] dark:hover:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5"
          :aria-label="mobileOpen ? $t('nav.aria_close_menu') : $t('nav.aria_open_menu')"
          @click="mobileOpen = !mobileOpen"
        >
          <svg v-if="!mobileOpen" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileOpen" class="md:hidden border-t border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-[#0F172A] px-6 py-4">
      <nav class="flex flex-col gap-3 mb-4">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="text-sm font-medium text-[#718096] dark:text-white/60 hover:text-[#1E3A5F] dark:hover:text-white"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </a>
      </nav>
      <div class="flex flex-col gap-2 border-t border-[#E2E8F0] dark:border-white/10 pt-4">
        <NuxtLink
          to="/login"
          class="rounded-lg border border-[#E2E8F0] dark:border-white/10 px-4 py-2 text-center text-sm font-semibold text-[#1E3A5F] dark:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5"
          @click="mobileOpen = false"
        >
          {{ $t('nav.login') }}
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="rounded-lg bg-[#1E3A5F] dark:bg-[#2E86AB] px-4 py-2 text-center text-sm font-semibold text-white hover:bg-[#2E4E7A] dark:hover:bg-[#3A9BC0]"
          @click="mobileOpen = false"
        >
          {{ $t('nav.start_free') }}
        </NuxtLink>
      </div>
    </div>
  </header>
</template>
