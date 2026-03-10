<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950">
    <div class="max-w-2xl mx-auto px-4 py-12">
      <div class="text-center mb-10">
        <NuxtLink to="/" class="inline-flex items-center gap-2">
          <UIcon name="i-lucide-scan-text" class="text-primary w-8 h-8" />
          <span class="text-2xl font-bold text-gray-900 dark:text-white">ATS Analyzer</span>
        </NuxtLink>
      </div>
      <slot />
    </div>
    <UNotifications />
  </div>
</template>
