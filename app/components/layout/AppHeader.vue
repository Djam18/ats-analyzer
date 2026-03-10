<script setup lang="ts">
const { user, signOut, loading } = useAuth()
const { t, locale, setLocale } = useI18n()

const items = computed(() => [[
  {
    label: user.value?.email ?? '',
    slot: 'account',
    disabled: true
  }
], [
  {
    label: t('nav.dashboard'),
    icon: 'i-lucide-layout-dashboard',
    to: '/dashboard'
  },
  {
    label: t('nav.myCvs'),
    icon: 'i-lucide-file-text',
    to: '/cvs'
  },
  {
    label: t('nav.history'),
    icon: 'i-lucide-history',
    to: '/analyses'
  }
], [
  {
    label: t('nav.settings'),
    icon: 'i-lucide-settings',
    to: '/settings'
  },
  {
    label: t('auth.logout'),
    icon: 'i-lucide-log-out',
    click: signOut
  }
]])

function toggleLocale() {
  setLocale(locale.value === 'fr' ? 'en' : 'fr')
}
</script>

<template>
  <header class="fixed top-0 left-0 right-0 z-40 h-16 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 flex items-center px-4 gap-3">
    <NuxtLink to="/dashboard" class="flex items-center gap-2 font-bold text-gray-900 dark:text-white lg:hidden">
      <UIcon name="i-lucide-scan-text" class="text-primary w-6 h-6" />
      ATS Analyzer
    </NuxtLink>
    <div class="flex-1" />

    <!-- Language toggle -->
    <UButton
      variant="ghost"
      color="neutral"
      size="sm"
      @click="toggleLocale"
    >
      {{ locale === 'fr' ? '🇬🇧 EN' : '🇫🇷 FR' }}
    </UButton>

    <UDropdownMenu :items="items">
      <UButton
        :loading="loading"
        variant="ghost"
        icon="i-lucide-user-circle"
        color="neutral"
      />
    </UDropdownMenu>
  </header>
</template>
