<script setup lang="ts">
definePageMeta({ middleware: 'guest', layout: 'auth' })

const { t } = useI18n()
const { signInWithEmail, signInWithGoogle, loading } = useAuth()

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })

function validate() {
  errors.email = ''
  errors.password = ''
  if (!form.email) errors.email = t('auth.errors.emailRequired')
  else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) errors.email = t('auth.errors.emailInvalid')
  if (!form.password) errors.password = t('auth.errors.passwordRequired')
  return !errors.email && !errors.password
}

async function handleSubmit() {
  if (!validate()) return
  await signInWithEmail(form.email, form.password)
}

function handleGoogleSignIn(): void {
  signInWithGoogle()
}
</script>

<template>
  <div>
    <div class="text-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ t('auth.login') }}
      </h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
        {{ t('auth.noAccount') }}
        <NuxtLink to="/register" class="text-primary font-medium hover:underline">
          {{ t('auth.register') }}
        </NuxtLink>
      </p>
    </div>

    <form class="space-y-4" @submit.prevent="handleSubmit">
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
          placeholder="••••••••"
          autocomplete="current-password"
          class="w-full"
        />
      </UFormField>

      <div class="flex justify-end">
        <NuxtLink to="/reset-password" class="text-sm text-primary hover:underline">
          {{ t('auth.forgotPassword') }}
        </NuxtLink>
      </div>

      <UButton type="submit" class="w-full" :loading="loading">
        {{ t('auth.signIn') }}
      </UButton>
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
      {{ t('auth.continueWithGoogle') }}
    </UButton>
  </div>
</template>
