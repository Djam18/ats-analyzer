<script setup lang="ts">
const route = useRoute()
const { t } = useI18n()
const isAdmin = ref(false)

onMounted(async () => {
  try {
    await $fetch('/api/admin/check')
    isAdmin.value = true
  }
  catch {
    isAdmin.value = false
  }
})

const navItems = computed(() => [
  { label: t('nav.dashboard'), icon: 'i-lucide-layout-dashboard', to: '/dashboard' },
  { label: t('nav.newAnalysis'), icon: 'i-lucide-plus-circle', to: '/analyses/new' },
  { label: t('nav.myCvs'), icon: 'i-lucide-file-text', to: '/cvs' },
  { label: t('nav.history'), icon: 'i-lucide-history', to: '/analyses' }
])

const bottomItems = computed(() => [
  { label: t('nav.pricing'), icon: 'i-lucide-credit-card', to: '/pricing' },
  { label: t('nav.settings'), icon: 'i-lucide-settings', to: '/settings' }
])

function isActive(to: string) {
  return route.path === to || (to !== '/analyses' && route.path.startsWith(to))
}
</script>

<template>
  <aside class="fixed top-16 left-0 bottom-0 w-64 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 flex flex-col pt-6 pb-4">
    <div class="px-3 mb-2">
      <NuxtLink to="/dashboard" class="flex items-center gap-2 px-3 py-2 font-bold text-gray-900 dark:text-white">
        <UIcon name="i-lucide-scan-text" class="text-primary w-6 h-6" />
        ATS Analyzer
      </NuxtLink>
    </div>

    <nav class="flex-1 px-3 space-y-1">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="isActive(item.to)
          ? 'bg-primary-50 dark:bg-primary-950 text-primary-600 dark:text-primary-400'
          : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
      >
        <UIcon :name="item.icon" class="w-5 h-5 flex-shrink-0" />
        {{ item.label }}
      </NuxtLink>
    </nav>

    <div class="px-3 space-y-1 border-t border-gray-200 dark:border-gray-800 pt-4">
      <NuxtLink
        v-for="item in bottomItems"
        :key="item.to"
        :to="item.to"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
      >
        <UIcon :name="item.icon" class="w-5 h-5 flex-shrink-0" />
        {{ item.label }}
      </NuxtLink>

      <NuxtLink
        v-if="isAdmin"
        to="/admin/stats"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="route.path.startsWith('/admin')
          ? 'bg-primary-50 dark:bg-primary-950 text-primary-600 dark:text-primary-400'
          : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
      >
        <UIcon name="i-lucide-shield" class="w-5 h-5 flex-shrink-0" />
        {{ t('nav.admin') }}
      </NuxtLink>
    </div>
  </aside>
</template>
