<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { t } = useI18n()
const { user, signOut } = useAuth()
const supabase = useSupabaseClient()
const toast = useToast()

const fullName = ref('')
const loading = ref(false)
const showDeleteConfirm = ref(false)
const deleteInput = ref('')
const deleting = ref(false)

const deleteWord = computed(() => t('settings.danger.deleteWord'))

onMounted(() => {
  fullName.value = (user.value?.user_metadata?.full_name as string) ?? ''
})

async function updateProfile() {
  loading.value = true
  try {
    const { error } = await supabase.auth.updateUser({
      data: { full_name: fullName.value.trim() }
    })
    if (error) throw error
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    await (supabase as any)
      .from('profiles')
      .update({ full_name: fullName.value.trim() })
      .eq('id', user.value?.id)
    toast.add({ title: t('settings.profile.save'), color: 'success' })
  }
  catch {
    toast.add({ title: t('common.error'), color: 'error' })
  }
  finally {
    loading.value = false
  }
}

async function handleDeleteAccount() {
  if (deleteInput.value !== deleteWord.value) return
  deleting.value = true
  try {
    await $fetch('/api/auth/delete-account', { method: 'POST' })
    await signOut()
  }
  catch {
    toast.add({ title: t('common.error'), color: 'error' })
    deleting.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
        {{ t('settings.title') }}
      </h1>
    </div>

    <UCard>
      <h2 class="font-semibold text-gray-900 dark:text-white mb-4">
        {{ t('settings.profile.title') }}
      </h2>
      <form class="space-y-4" @submit.prevent="updateProfile">
        <UFormField :label="t('settings.profile.fullName')">
          <UInput v-model="fullName" class="w-full" />
        </UFormField>
        <UFormField :label="t('auth.email')">
          <UInput :model-value="user?.email" disabled class="w-full" />
        </UFormField>
        <UButton type="submit" :loading="loading">
          {{ t('settings.profile.save') }}
        </UButton>
      </form>
    </UCard>

    <UCard>
      <h2 class="font-semibold text-gray-900 dark:text-white mb-3">
        {{ t('settings.billing.title') }}
      </h2>
      <NuxtLink to="/settings/billing" class="flex items-center justify-between text-sm text-gray-700 dark:text-gray-300 hover:text-primary transition-colors">
        <span>{{ t('settings.billing.manage') }}</span>
        <UIcon name="i-lucide-chevron-right" class="w-4 h-4" />
      </NuxtLink>
    </UCard>

    <UCard class="border-red-200 dark:border-red-900">
      <h2 class="font-semibold text-red-600 dark:text-red-400 mb-2">
        {{ t('settings.danger.title') }}
      </h2>
      <p class="text-sm text-gray-500 mb-4">
        {{ t('settings.danger.deleteAccount') }}
      </p>
      <UButton color="error" variant="outline" @click="showDeleteConfirm = true">
        {{ t('settings.danger.deleteAccount') }}
      </UButton>
    </UCard>

    <UModal v-model:open="showDeleteConfirm">
      <template #content>
        <div class="p-6">
          <h3 class="text-lg font-bold text-red-600 mb-2">
            {{ t('settings.danger.deleteAccount') }}
          </h3>
          <p class="text-sm text-gray-500 mb-4">
            {{ t('settings.danger.deleteConfirm') }} <strong>{{ deleteWord }}</strong>
          </p>
          <UInput
            v-model="deleteInput"
            :placeholder="deleteWord"
            class="w-full mb-4"
          />
          <div class="flex justify-end gap-3">
            <UButton variant="ghost" color="neutral" @click="showDeleteConfirm = false">
              {{ t('common.cancel') }}
            </UButton>
            <UButton
              color="error"
              :disabled="deleteInput !== deleteWord"
              :loading="deleting"
              @click="handleDeleteAccount"
            >
              {{ t('common.confirm') }}
            </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
