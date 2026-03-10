<script setup lang="ts">
const scrolled = ref(false)
const mobileOpen = ref(false)

const navLinks = [
  { label: 'Fonctionnalités', href: '#features' },
  { label: 'Tarifs', href: '#pricing' },
  { label: 'FAQ', href: '#faq' },
]

onMounted(() => {
  const handler = () => { scrolled.value = window.scrollY > 10 }
  window.addEventListener('scroll', handler, { passive: true })
  onUnmounted(() => window.removeEventListener('scroll', handler))
})
</script>

<template>
  <header
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-200',
      scrolled ? 'bg-white border-b border-[#E2E8F0] shadow-[0_1px_3px_rgba(0,0,0,0.08)]' : 'bg-white/90 backdrop-blur-sm',
    ]"
  >
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
      <!-- Logo -->
      <SharedLogo size="md" />

      <!-- Nav desktop -->
      <nav class="hidden md:flex items-center gap-6">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="text-sm font-medium text-[#718096] hover:text-[#1E3A5F] transition-colors"
        >
          {{ link.label }}
        </a>
      </nav>

      <!-- CTA desktop -->
      <div class="hidden md:flex items-center gap-3">
        <NuxtLink
          to="/login"
          class="text-sm font-medium text-[#1E3A5F] hover:text-[#2E86AB] transition-colors px-3 py-2"
        >
          Connexion
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="rounded-lg bg-[#1E3A5F] px-4 py-2 text-sm font-semibold text-white hover:bg-[#2E4E7A] transition-colors"
        >
          Commencer gratuitement
        </NuxtLink>
      </div>

      <!-- Hamburger mobile -->
      <button
        class="md:hidden p-2 rounded-md text-[#718096] hover:text-[#1E3A5F] hover:bg-[#F8F9FA]"
        @click="mobileOpen = !mobileOpen"
        aria-label="Menu"
      >
        <svg v-if="!mobileOpen" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
        <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileOpen" class="md:hidden border-t border-[#E2E8F0] bg-white px-6 py-4">
      <nav class="flex flex-col gap-3 mb-4">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="text-sm font-medium text-[#718096] hover:text-[#1E3A5F]"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </a>
      </nav>
      <div class="flex flex-col gap-2 border-t border-[#E2E8F0] pt-4">
        <NuxtLink
          to="/login"
          class="rounded-lg border border-[#E2E8F0] px-4 py-2 text-center text-sm font-semibold text-[#1E3A5F] hover:bg-[#F8F9FA]"
          @click="mobileOpen = false"
        >
          Connexion
        </NuxtLink>
        <NuxtLink
          to="/register"
          class="rounded-lg bg-[#1E3A5F] px-4 py-2 text-center text-sm font-semibold text-white hover:bg-[#2E4E7A]"
          @click="mobileOpen = false"
        >
          Commencer gratuitement
        </NuxtLink>
      </div>
    </div>
  </header>
</template>
