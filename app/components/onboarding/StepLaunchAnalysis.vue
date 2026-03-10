<script setup lang="ts">
defineProps<{ cvId: string }>()
const emit = defineEmits<{ complete: [] }>()

const supabase = useSupabaseClient()
const user = useSupabaseUser()

async function handleComplete() {
  if (!user.value) return
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  await (supabase as any)
    .from('profiles')
    .update({ onboarding_completed: true })
    .eq('id', user.value.id)
  emit('complete')
  await navigateTo('/analyses/new')
}
</script>

<template>
  <div class="py-8 text-center">
    <div class="w-20 h-20 bg-primary-50 dark:bg-primary-950 rounded-full flex items-center justify-center mx-auto mb-6">
      <UIcon name="i-lucide-scan-text" class="w-10 h-10 text-primary" />
    </div>

    <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
      Vous êtes prêt !
    </h2>
    <p class="text-gray-500 dark:text-gray-400 text-sm max-w-sm mx-auto mb-8">
      Votre CV est chargé. Lancez maintenant votre première analyse ATS et découvrez votre score de compatibilité.
    </p>

    <div class="grid grid-cols-3 gap-4 mb-8 text-center">
      <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div class="text-2xl font-bold text-primary mb-1">
          3
        </div>
        <div class="text-xs text-gray-500">
          analyses gratuites
        </div>
      </div>
      <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div class="text-2xl font-bold text-primary mb-1">
          0-100
        </div>
        <div class="text-xs text-gray-500">
          score ATS
        </div>
      </div>
      <div class="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
        <div class="text-2xl font-bold text-primary mb-1">
          &lt;30s
        </div>
        <div class="text-xs text-gray-500">
          résultats
        </div>
      </div>
    </div>

    <UButton size="lg" icon="i-lucide-zap" @click="handleComplete">
      Lancer ma première analyse
    </UButton>
  </div>
</template>
