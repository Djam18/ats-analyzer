<template>
  <div class="min-h-screen bg-[#F8F9FA] flex flex-col items-center justify-center px-4 py-12">
    <!-- Card -->
    <div class="w-full max-w-sm rounded-xl border border-[#E2E8F0] bg-white p-8 shadow-[0_4px_12px_rgba(0,0,0,0.08)]">
      <!-- Logo -->
      <div class="mb-8 flex justify-center">
        <SharedLogo size="lg" />
      </div>

      <!-- Success state -->
      <template v-if="sent">
        <div class="text-center">
          <div class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-full bg-[#F0FFF4]">
            <svg class="h-6 w-6 text-[#38A169]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 class="mb-2 text-xl font-bold text-[#1A202C]">{{ $t('forgot_password.success_title') }}</h2>
          <p class="text-sm text-[#718096]">{{ $t('forgot_password.success_body') }}</p>
        </div>
      </template>

      <!-- Form state -->
      <template v-else>
        <h1 class="mb-1 text-2xl font-bold text-[#1A202C] text-center">{{ $t('forgot_password.title') }}</h1>
        <p class="mb-7 text-center text-sm text-[#718096]">{{ $t('forgot_password.subtitle') }}</p>

        <form class="space-y-4" @submit.prevent="handleSubmit">
          <div>
            <label for="forgot-email" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
              {{ $t('forgot_password.email_label') }}
            </label>
            <input
              id="forgot-email"
              v-model="email"
              type="email"
              :placeholder="$t('forgot_password.email_placeholder')"
              autocomplete="email"
              required
              class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
            />
          </div>

          <button
            type="submit"
            class="mt-2 w-full rounded-lg bg-[#1E3A5F] py-2.5 text-sm font-semibold text-white hover:bg-[#2E4E7A] transition-colors"
          >
            {{ $t('forgot_password.submit') }}
          </button>
        </form>
      </template>
    </div>

    <NuxtLink to="/login" class="mt-6 text-xs text-[#718096] hover:text-[#1E3A5F] transition-colors">
      {{ $t('forgot_password.back_login') }}
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({ title: () => t('forgot_password.page_title') })

const email = ref('')
const sent = ref(false)

// TODO: implement password reset (Phase 2)
function handleSubmit() {
  if (!email.value) return
  sent.value = true
}
</script>
