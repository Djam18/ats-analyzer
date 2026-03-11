<template>
  <NuxtPage />
</template>

<script setup lang="ts">
const { init } = useDarkMode()
onMounted(init)
</script>
