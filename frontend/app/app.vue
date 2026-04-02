<template>
  <NuxtPage />
</template>

<script setup lang="ts">
const { init } = useDarkMode()
const { initSession } = useAuth()

onMounted(async () => {
  init()
  await initSession()
})
</script>
