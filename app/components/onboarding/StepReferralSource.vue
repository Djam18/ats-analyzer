<script setup lang="ts">
const emit = defineEmits<{ done: [] }>()

const { t, locale, setLocale } = useI18n()
const supabase = useSupabaseClient()
const user = useSupabaseUser()
const loading = ref(false)
const selected = ref<string | null>(null)

const languages = [
  { code: 'fr', label: 'Français', flag: '🇫🇷' },
  { code: 'en', label: 'English', flag: '🇬🇧' }
]

const sources = computed(() => [
  { value: 'word_of_mouth', label: t('onboarding.referral.sources.word_of_mouth'), icon: 'i-lucide-users' },
  { value: 'linkedin', label: t('onboarding.referral.sources.linkedin'), icon: 'i-simple-icons-linkedin' },
  { value: 'google', label: t('onboarding.referral.sources.google'), icon: 'i-simple-icons-google' },
  { value: 'youtube_blog', label: t('onboarding.referral.sources.youtube_blog'), icon: 'i-lucide-play-circle' },
  { value: 'twitter', label: t('onboarding.referral.sources.twitter'), icon: 'i-simple-icons-x' },
  { value: 'other', label: t('onboarding.referral.sources.other'), icon: 'i-lucide-more-horizontal' }
])

async function handleSetLocale(code: string) {
  await setLocale(code as 'fr' | 'en')
  if (user.value) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    await (supabase as any)
      .from('profiles')
      .update({ locale: code })
      .eq('id', user.value.id)
  }
}

async function handleContinue() {
  if (!user.value) return
  loading.value = true
  try {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    await (supabase as any)
      .from('profiles')
      .update({ referral_source: selected.value ?? 'other' })
      .eq('id', user.value.id)
  }
  catch {
    // Non-blocking — don't stop the user
  }
  finally {
    loading.value = false
    emit('done')
  }
}
</script>

<template>
  <div class="py-2">
    <div class="text-center mb-8">
      <div class="w-14 h-14 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <UIcon name="i-lucide-heart-handshake" class="w-7 h-7 text-primary" />
      </div>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
        {{ t('onboarding.referral.title') }}
      </h2>
      <p class="text-sm text-gray-500">
        {{ t('onboarding.referral.subtitle') }} {{ t('onboarding.referral.optional') }}
      </p>
    </div>

    <!-- Language selector -->
    <div class="mb-6">
      <p class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
        {{ t('onboarding.referral.language') }}
      </p>
      <div class="flex gap-2">
        <button
          v-for="lang in languages"
          :key="lang.code"
          type="button"
          class="flex items-center gap-2 px-4 py-2 rounded-lg border-2 text-sm font-medium transition-all"
          :class="locale === lang.code
            ? 'border-primary bg-primary/5 text-primary'
            : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-gray-300'"
          @click="handleSetLocale(lang.code)"
        >
          <span>{{ lang.flag }}</span>
          {{ lang.label }}
        </button>
      </div>
      <p class="text-xs text-gray-400 mt-1">
        {{ t('onboarding.referral.languageHint') }}
      </p>
    </div>

    <!-- Referral sources -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
      <button
        v-for="source in sources"
        :key="source.value"
        type="button"
        class="flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all text-sm font-medium"
        :class="selected === source.value
          ? 'border-primary bg-primary/5 text-primary'
          : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-gray-300 dark:hover:border-gray-600'"
        @click="selected = source.value"
      >
        <UIcon :name="source.icon" class="w-6 h-6" />
        {{ source.label }}
      </button>
    </div>

    <UButton
      block
      :loading="loading"
      @click="handleContinue"
    >
      {{ t('onboarding.referral.continue') }}
    </UButton>
  </div>
</template>
