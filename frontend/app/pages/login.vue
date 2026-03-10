<template>
  <div class="min-h-screen bg-[#F8F9FA] flex flex-col items-center justify-center px-4 py-12">
    <!-- Card -->
    <div class="w-full max-w-sm rounded-xl border border-[#E2E8F0] bg-white p-8 shadow-[0_4px_12px_rgba(0,0,0,0.08)]">
      <!-- Logo -->
      <div class="mb-8 flex justify-center">
        <SharedLogo size="lg" />
      </div>

      <h1 class="mb-1 text-2xl font-bold text-[#1A202C] text-center">Connexion</h1>
      <p class="mb-7 text-center text-sm text-[#718096]">Accédez à votre espace recruteur</p>

      <form class="space-y-4" @submit.prevent>
        <!-- Email -->
        <div>
          <label class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            Email
          </label>
          <input
            v-model="form.email"
            type="email"
            placeholder="email@entreprise.com"
            class="w-full rounded-md border border-[#E2E8F0] bg-white px-3 py-2.5 text-sm text-[#1A202C] placeholder-[#718096] outline-none focus:border-[#2E86AB] focus:ring-2 focus:ring-[#2E86AB]/20 transition-colors"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#718096]">
            Mot de passe
          </label>
          <input
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
          Se connecter
        </button>
      </form>

      <div class="mt-5 text-center">
        <a href="#" class="text-xs text-[#2E86AB] hover:underline">
          Mot de passe oublié ?
        </a>
      </div>

      <div class="mt-6 border-t border-[#E2E8F0] pt-5 text-center">
        <p class="text-sm text-[#718096]">
          Pas encore de compte ?
          <NuxtLink to="/register" class="font-semibold text-[#1E3A5F] hover:text-[#2E86AB] transition-colors">
            Créer un compte
          </NuxtLink>
        </p>
      </div>
    </div>

    <!-- Back to home -->
    <NuxtLink to="/" class="mt-6 text-xs text-[#718096] hover:text-[#1E3A5F] transition-colors">
      ← Retour à l'accueil
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
useHead({ title: 'Connexion — ATS Platform' })

const form = reactive({
  email: '',
  password: '',
})
</script>
