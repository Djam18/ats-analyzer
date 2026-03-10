<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

const { resetPassword, loading } = useAuth()

const email = ref('')
const emailError = ref('')
const sent = ref(false)

async function handleSubmit() {
  emailError.value = ''
  if (!email.value) {
    emailError.value = 'L\'email est requis'
    return
  }
  await resetPassword(email.value)
  sent.value = true
}
</script>

<template>
  <div>
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        Mot de passe oublié
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        Entrez votre email pour recevoir un lien de réinitialisation
      </p>
    </div>

    <div v-if="sent" class="text-center py-4">
      <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <UIcon name="i-lucide-mail-check" class="w-8 h-8 text-green-600" />
      </div>
      <p class="text-gray-600 dark:text-gray-400 text-sm mb-6">
        Si ce compte existe, un email de réinitialisation a été envoyé.
      </p>
      <NuxtLink to="/login" class="text-primary text-sm font-medium hover:underline">
        Retour à la connexion
      </NuxtLink>
    </div>

    <form v-else class="space-y-4" @submit.prevent="handleSubmit">
      <UFormField label="Email" :error="emailError">
        <UInput
          v-model="email"
          type="email"
          placeholder="vous@exemple.com"
          autocomplete="email"
          class="w-full"
        />
      </UFormField>

      <UButton type="submit" class="w-full" :loading="loading">
        Envoyer le lien
      </UButton>

      <div class="text-center">
        <NuxtLink to="/login" class="text-sm text-gray-500 hover:text-primary">
          Retour à la connexion
        </NuxtLink>
      </div>
    </form>
  </div>
</template>
