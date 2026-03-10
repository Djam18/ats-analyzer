<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const route = useRoute()
const supabase = useSupabaseClient()
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const type = route.query.type as string

  if (type === 'recovery') {
    // Password reset flow — user arrives with token in URL hash
    // Supabase handles session automatically
    await navigateTo('/settings/password')
    return
  }

  // Email confirmation or OAuth callback
  const { error: sessionError } = await supabase.auth.getSession()
  if (sessionError) {
    error.value = 'Lien invalide ou expiré. Veuillez recommencer.'
  }
  else {
    // Fire welcome email (non-blocking, idempotent server route)
    fetch('/api/auth/send-welcome', { method: 'POST' }).catch(() => {})
    await navigateTo('/onboarding')
  }
  loading.value = false
})
</script>

<template>
  <div class="text-center py-8">
    <div v-if="loading">
      <UIcon name="i-lucide-loader-2" class="w-10 h-10 animate-spin text-primary mx-auto mb-4" />
      <p class="text-gray-500">
        Vérification en cours...
      </p>
    </div>
    <div v-else-if="error">
      <UIcon name="i-lucide-x-circle" class="w-10 h-10 text-error mx-auto mb-4" />
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        {{ error }}
      </p>
      <NuxtLink to="/login" class="text-primary hover:underline">
        Retour à la connexion
      </NuxtLink>
    </div>
  </div>
</template>
