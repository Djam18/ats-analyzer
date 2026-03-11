<template>
  <div class="min-h-screen bg-[#F8F9FA] flex flex-col items-center justify-center px-4 py-12">
    <!-- Card -->
    <div class="w-full max-w-sm rounded-xl border border-[#E2E8F0] bg-white p-8 shadow-[0_4px_12px_rgba(0,0,0,0.08)]">
      <!-- Logo -->
      <div class="mb-8 flex justify-center">
        <SharedLogo size="lg" />
      </div>

      <h1 class="mb-1 text-2xl font-bold text-[#1A202C] text-center">{{ $t('login.title') }}</h1>
      <p class="mb-7 text-center text-sm text-[#718096]">{{ $t('login.subtitle') }}</p>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <!-- Email -->
        <div>
          <label for="login-email" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            {{ $t('login.email_label') }}
          </label>
          <input
            id="login-email"
            v-model="form.email"
            type="email"
            :placeholder="$t('login.email_placeholder')"
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- Password -->
        <div>
          <label for="login-password" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            {{ $t('login.password_label') }}
          </label>
          <input
            id="login-password"
            v-model="form.password"
            type="password"
            placeholder="••••••••"
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- CTA -->
        <button
          type="submit"
          class="mt-2 w-full rounded-lg bg-[#1E3A5F] py-2.5 text-sm font-semibold text-white hover:bg-[#2E4E7A] transition-colors"
        >
          {{ $t('login.submit') }}
        </button>
      </form>

      <div class="mt-5 text-center">
        <NuxtLink to="/auth/forgot-password" class="text-xs text-[#2E86AB] hover:underline">
          {{ $t('login.forgot_password') }}
        </NuxtLink>
      </div>

      <div class="mt-6 border-t border-[#E2E8F0] pt-5 text-center">
        <p class="text-sm text-[#718096]">
          {{ $t('login.no_account') }}
          <NuxtLink to="/register" class="font-semibold text-[#1E3A5F] hover:text-[#2E86AB] transition-colors">
            {{ $t('login.create_account') }}
          </NuxtLink>
        </p>
      </div>
    </div>

    <!-- Back to home -->
    <NuxtLink to="/" class="mt-6 text-xs text-[#718096] hover:text-[#1E3A5F] transition-colors">
      {{ $t('login.back_home') }}
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({ title: () => t('login.page_title') })

const form = reactive({
  email: '',
  password: '',
})

// TODO: implement auth (Phase 2)
function handleLogin() {}

</script>
