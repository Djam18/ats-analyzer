<script setup lang="ts">
definePageMeta({ middleware: 'guest', layout: 'auth' })

const { t } = useI18n()
const { signUpWithEmail, signInWithGoogle, loading } = useAuth()

const form = reactive({ fullName: '', email: '', password: '' })
const errors = reactive({ fullName: '', email: '', password: '' })

function validate() {
  errors.fullName = ''
  errors.email = ''
  errors.password = ''
  if (!form.fullName.trim()) errors.fullName = t('auth.errors.nameRequired')
  if (!form.email) errors.email = t('auth.errors.emailRequired')
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.email = t('auth.errors.emailInvalid')
  if (!form.password) errors.password = t('auth.errors.passwordRequired')
  else if (form.password.length < 8) errors.password = t('auth.errors.passwordMinLength')
  else if (!/[A-Z]/.test(form.password)) errors.password = t('auth.errors.passwordUppercase')
  else if (!/[0-9]/.test(form.password)) errors.password = t('auth.errors.passwordDigit')
  return !errors.fullName && !errors.email && !errors.password
}

async function handleSubmit() {
  if (!validate()) return
  await signUpWithEmail(form.email, form.password, form.fullName)
}

function handleGoogleSignIn(): void {
  signInWithGoogle()
}
</script>

<template>
  <div>
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ t('auth.register') }}
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        {{ t('auth.alreadyAccount') }}
        <NuxtLink to="/login" class="text-primary font-medium hover:underline">
          {{ t('auth.signIn') }}
        </NuxtLink>
      </p>
    </div>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <UFormField :label="t('auth.fullName')" :error="errors.fullName">
        <UInput
          v-model="form.fullName"
          :placeholder="t('auth.namePlaceholder')"
          autocomplete="name"
          class="w-full"
        />
      </UFormField>

      <UFormField :label="t('auth.email')" :error="errors.email">
        <UInput
          v-model="form.email"
          type="email"
          :placeholder="t('auth.emailPlaceholder')"
          autocomplete="email"
          class="w-full"
        />
      </UFormField>

      <UFormField :label="t('auth.password')" :error="errors.password">
        <UInput
          v-model="form.password"
          type="password"
          :placeholder="t('auth.passwordHint')"
          autocomplete="new-password"
          class="w-full"
        />
      </UFormField>

      <UButton type="submit" class="w-full" :loading="loading">
        {{ t('auth.createAccount') }}
      </UButton>

      <p class="text-xs text-center text-gray-400">
        {{ t('auth.terms') }}
        <NuxtLink to="/terms" class="text-primary hover:underline">
          {{ t('auth.termsLink') }}
        </NuxtLink>
      </p>
    </form>

    <div class="relative my-6">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-200 dark:border-gray-700" />
      </div>
      <div class="relative flex justify-center text-xs uppercase">
        <span class="bg-white dark:bg-gray-900 px-2 text-gray-500">{{ t('common.or') }}</span>
      </div>
    </div>

    <UButton
      variant="outline"
      color="neutral"
      class="w-full"
      icon="i-simple-icons-google"
      :loading="loading"
      @click="handleGoogleSignIn"
    >
      {{ t('auth.registerWithGoogle') }}
    </UButton>
  </div>
</template>
