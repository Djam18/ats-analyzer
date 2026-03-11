<template>
  <div class="min-h-screen bg-[#F8F9FA] flex flex-col items-center justify-center px-4 py-12">
    <!-- Card -->
    <div class="w-full max-w-sm rounded-xl border border-[#E2E8F0] bg-white p-8 shadow-[0_4px_12px_rgba(0,0,0,0.08)]">
      <!-- Logo -->
      <div class="mb-8 flex justify-center">
        <SharedLogo size="lg" />
      </div>

      <h1 class="mb-1 text-2xl font-bold text-[#1A202C] text-center">{{ $t('register.title') }}</h1>
      <p class="mb-7 text-center text-sm text-[#718096]">{{ $t('register.subtitle') }}</p>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <!-- First name + Last name -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label for="register-first-name" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
              {{ $t('register.first_name_label') }}
            </label>
            <input
              id="register-first-name"
              v-model="form.firstName"
              type="text"
              :placeholder="$t('register.first_name_placeholder')"
              autocomplete="given-name"
              required
              class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
            />
          </div>
          <div>
            <label for="register-last-name" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
              {{ $t('register.last_name_label') }}
            </label>
            <input
              id="register-last-name"
              v-model="form.lastName"
              type="text"
              :placeholder="$t('register.last_name_placeholder')"
              autocomplete="family-name"
              required
              class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
            />
          </div>
        </div>

        <!-- Email -->
        <div>
          <label for="register-email" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            {{ $t('register.email_label') }}
          </label>
          <input
            id="register-email"
            v-model="form.email"
            type="email"
            :placeholder="$t('register.email_placeholder')"
            autocomplete="email"
            required
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- Company -->
        <div>
          <label for="register-company" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            {{ $t('register.company_label') }}
          </label>
          <input
            id="register-company"
            v-model="form.company"
            type="text"
            :placeholder="$t('register.company_placeholder')"
            autocomplete="organization"
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- Password -->
        <div>
          <label for="register-password" class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            {{ $t('register.password_label') }}
          </label>
          <input
            id="register-password"
            v-model="form.password"
            type="password"
            :placeholder="$t('register.password_placeholder')"
            autocomplete="new-password"
            required
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- CTA -->
        <button
          type="submit"
          class="mt-2 w-full rounded-lg bg-[#1E3A5F] py-2.5 text-sm font-semibold text-white hover:bg-[#2E4E7A] transition-colors"
        >
          {{ $t('register.submit') }}
        </button>
      </form>

      <p class="mt-4 text-center text-xs text-[#718096]">
        {{ $t('register.terms_prefix') }}
        <NuxtLink to="/legal/terms" class="text-[#2E86AB] hover:underline">{{ $t('register.terms_link') }}</NuxtLink>
        {{ $t('register.privacy_conjunction') }}
        <NuxtLink to="/legal/privacy" class="text-[#2E86AB] hover:underline">{{ $t('register.privacy_link') }}</NuxtLink>.
      </p>

      <div class="mt-5 border-t border-[#E2E8F0] pt-5 text-center">
        <p class="text-sm text-[#718096]">
          {{ $t('register.already_account') }}
          <NuxtLink to="/login" class="font-semibold text-[#1E3A5F] hover:text-[#2E86AB] transition-colors">
            {{ $t('register.login_link') }}
          </NuxtLink>
        </p>
      </div>
    </div>

    <!-- Back to home -->
    <NuxtLink to="/" class="mt-6 text-xs text-[#718096] hover:text-[#1E3A5F] transition-colors">
      {{ $t('register.back_home') }}
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({ title: () => t('register.page_title') })

const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  company: '',
  password: '',
})

// TODO: implement auth (Phase 2)
function handleRegister() {}
</script>
