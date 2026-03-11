<template>
  <section id="pricing" class="py-20 bg-white dark:bg-[#0F172A]">
    <div class="mx-auto max-w-6xl px-6">
      <div class="mb-12 text-center">
        <p class="mb-3 text-xs font-semibold uppercase tracking-widest text-[#2E86AB]">{{ $t('pricing.label') }}</p>
        <h2 class="text-3xl font-bold text-[#1A202C] dark:text-white md:text-4xl">{{ $t('pricing.title') }}</h2>
        <p class="mx-auto mt-4 max-w-xl text-[#718096] dark:text-white/60">
          {{ $t('pricing.subtitle') }}
        </p>
      </div>

      <!-- Loading skeleton -->
      <div v-if="status === 'pending'" class="grid gap-6 md:grid-cols-3">
        <div
          v-for="i in 3"
          :key="i"
          class="flex flex-col rounded-xl border border-[#E2E8F0] dark:border-white/10 p-6 animate-pulse"
        >
          <div class="mb-5 space-y-2">
            <div class="h-4 w-24 rounded bg-[#E2E8F0] dark:bg-white/10" />
            <div class="h-3 w-36 rounded bg-[#E2E8F0] dark:bg-white/10" />
          </div>
          <div class="mb-6">
            <div class="h-10 w-28 rounded bg-[#E2E8F0] dark:bg-white/10" />
          </div>
          <div class="mb-7 flex-1 space-y-3">
            <div v-for="j in 5" :key="j" class="h-3 w-full rounded bg-[#E2E8F0] dark:bg-white/10" />
          </div>
          <div class="h-10 w-full rounded-lg bg-[#E2E8F0] dark:bg-white/10" />
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="mb-8 rounded-xl border border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/30 p-4 text-center text-sm text-red-600 dark:text-red-400">
        {{ $t('pricing.error') }}
      </div>

      <!-- Plans grid -->
      <div v-else class="grid gap-6 md:grid-cols-3">
        <div
          v-for="plan in plans"
          :key="plan.id"
          :class="[
            'relative flex flex-col rounded-xl border p-6',
            plan.highlighted
              ? 'border-[#2E86AB] bg-white dark:bg-[#1E293B] shadow-[0_4px_12px_rgba(46,134,171,0.15)]'
              : 'border-[#E2E8F0] dark:border-white/10 bg-white dark:bg-[#1E293B] shadow-[0_1px_3px_rgba(0,0,0,0.08)]',
          ]"
        >
          <!-- Popular badge -->
          <div v-if="plan.highlighted" class="absolute -top-3 left-1/2 -translate-x-1/2">
            <span class="rounded-full bg-[#2E86AB] px-3 py-1 text-xs font-bold text-white">{{ $t('pricing.popular') }}</span>
          </div>

          <div class="mb-5">
            <h3 class="mb-1 text-base font-bold text-[#1A202C] dark:text-white">{{ plan.name }}</h3>
            <p class="text-xs text-[#718096] dark:text-white/50">{{ plan.desc }}</p>
          </div>

          <!-- Price -->
          <div class="mb-6">
            <div class="flex items-end gap-1">
              <span class="font-mono text-4xl font-bold text-[#1E3A5F] dark:text-white">{{ plan.price }}</span>
              <span v-if="plan.period" class="mb-1 text-sm text-[#718096] dark:text-white/50">{{ plan.period }}</span>
            </div>
            <p v-if="plan.note" class="mt-1 text-xs font-semibold text-[#38A169]">{{ plan.note }}</p>
          </div>

          <!-- Features -->
          <ul class="mb-7 flex-1 space-y-3">
            <li v-for="feature in plan.features" :key="feature" class="flex items-start gap-2.5">
              <svg
                class="mt-0.5 h-4 w-4 flex-shrink-0 text-[#38A169]"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-sm text-[#718096] dark:text-white/60">{{ feature }}</span>
            </li>
          </ul>

          <!-- CTA -->
          <NuxtLink
            :to="plan.cta.href"
            :class="[
              'block rounded-lg px-4 py-2.5 text-center text-sm font-semibold transition-colors',
              plan.highlighted
                ? 'bg-[#1E3A5F] text-white hover:bg-[#2E4E7A]'
                : 'border border-[#E2E8F0] dark:border-white/10 text-[#1E3A5F] dark:text-white hover:bg-[#F8F9FA] dark:hover:bg-white/5',
            ]"
          >
            {{ plan.cta.label }}
          </NuxtLink>
        </div>
      </div>

      <p class="mt-8 text-center text-xs text-[#718096] dark:text-white/40">
        {{ $t('pricing.footer_note') }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
interface StripePlan {
  id: string
  name: string
  description: string | null
  amount: number
  currency: string
  interval: string | null
  metadata: Record<string, string>
}

const { t } = useI18n()

const enterprisePlan = computed(() => ({
  id: 'enterprise',
  name: t('pricing.enterprise_name'),
  desc: t('pricing.enterprise_desc'),
  price: t('pricing.enterprise_price'),
  period: '',
  note: null,
  highlighted: false,
  features: [
    t('pricing.enterprise_f1'),
    t('pricing.enterprise_f2'),
    t('pricing.enterprise_f3'),
    t('pricing.enterprise_f4'),
    t('pricing.enterprise_f5'),
    t('pricing.enterprise_f6'),
  ],
  cta: { label: t('pricing.enterprise_cta'), href: '/register' },
}))

const planConfig = computed(() => ({
  Basic: {
    desc: t('pricing.basic_desc'),
    note: t('pricing.basic_note'),
    highlighted: false,
    features: [
      t('pricing.basic_f1'),
      t('pricing.basic_f2'),
      t('pricing.basic_f3'),
      t('pricing.basic_f4'),
      t('pricing.basic_f5'),
      t('pricing.basic_f6'),
    ],
    cta: { label: t('pricing.basic_cta'), href: '/register' },
  },
  Pro: {
    desc: t('pricing.pro_desc'),
    note: null,
    highlighted: true,
    features: [
      t('pricing.pro_f1'),
      t('pricing.pro_f2'),
      t('pricing.pro_f3'),
      t('pricing.pro_f4'),
      t('pricing.pro_f5'),
      t('pricing.pro_f6'),
      t('pricing.pro_f7'),
    ],
    cta: { label: t('pricing.pro_cta'), href: '/register' },
  },
}))

const { data, status, error } = useFetch<StripePlan[]>('/api/pricing')

const plans = computed(() => {
  const stripePlans = (data.value ?? []).map((stripe) => {
    const config = (planConfig.value as Record<string, typeof planConfig.value.Basic>)[stripe.name] ?? {
      desc: stripe.description ?? '',
      note: null,
      highlighted: false,
      features: [],
      cta: { label: t('pricing.cta_start'), href: '/register' },
    }

    const isFreePlan = stripe.amount === 0
    const price = isFreePlan
      ? '0€'
      : `${stripe.amount.toLocaleString('fr-FR')}${stripe.currency === 'EUR' ? '€' : ` ${stripe.currency}`}`

    const period = stripe.interval
      ? stripe.interval === 'month'
        ? t('pricing.period_month')
        : stripe.interval === 'year'
          ? t('pricing.period_year')
          : `/ ${stripe.interval}`
      : ''

    return { id: stripe.id, name: stripe.name, price, period, ...config }
  })

  return [...stripePlans, enterprisePlan.value]
})
</script>
