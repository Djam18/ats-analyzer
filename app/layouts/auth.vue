<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <NuxtLink to="/" class="inline-flex items-center gap-2">
          <UIcon name="i-lucide-scan-text" class="text-primary w-8 h-8" />
          <span class="text-2xl font-bold text-gray-900 dark:text-white">ATS Analyzer</span>
        </NuxtLink>
      </div>
      <UCard>
        <slot />
      </UCard>
    </div>
  </div>
</template>
