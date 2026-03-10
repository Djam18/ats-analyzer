<script setup lang="ts">
defineProps<{
  keywords: Array<{ keyword: string, context?: string }>
}>()
</script>

<template>
  <div>
    <div class="flex items-center gap-2 mb-3">
      <UIcon name="i-lucide-check-circle" class="w-5 h-5 text-green-500" />
      <h3 class="font-semibold text-gray-900 dark:text-white">
        Mots-clés trouvés
      </h3>
      <UBadge color="success" variant="soft" size="sm">
        {{ keywords.length }}
      </UBadge>
    </div>

    <div v-if="keywords.length === 0" class="text-sm text-gray-400 italic">
      Aucun mot-clé correspondant détecté.
    </div>

    <div v-else class="flex flex-wrap gap-2">
      <div
        v-for="kw in keywords"
        :key="kw.keyword"
        class="group relative"
      >
        <span
          class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800 dark:bg-green-950 dark:text-green-300 cursor-default"
          :title="kw.context"
        >
          <UIcon name="i-lucide-check" class="w-3 h-3 mr-1.5" />
          {{ kw.keyword }}
        </span>
      </div>
    </div>
  </div>
</template>
