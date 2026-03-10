export const useAuth = () => {
  const supabase = useSupabaseClient()
  const user = useSupabaseUser()
  const toast = useToast()

  const loading = ref(false)

  async function signUpWithEmail(email: string, password: string, fullName: string) {
    loading.value = true
    try {
      const { error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: { full_name: fullName },
          emailRedirectTo: `${window.location.origin}/confirm`
        }
      })
      if (error) throw error
      toast.add({ title: 'Vérifiez votre email', description: 'Un lien de confirmation vous a été envoyé.', color: 'success' })
      return { success: true }
    }
    catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Erreur lors de l\'inscription'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
      return { success: false, error: message }
    }
    finally {
      loading.value = false
    }
  }

  async function signInWithEmail(email: string, password: string) {
    loading.value = true
    try {
      const { error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) throw error
      await navigateTo('/dashboard')
      return { success: true }
    }
    catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Identifiants incorrects'
      toast.add({ title: 'Connexion échouée', description: message, color: 'error' })
      return { success: false, error: message }
    }
    finally {
      loading.value = false
    }
  }

  async function signInWithGoogle() {
    loading.value = true
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: { redirectTo: `${window.location.origin}/confirm` }
      })
      if (error) throw error
      return { success: true }
    }
    catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Erreur OAuth Google'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
      return { success: false, error: message }
    }
    finally {
      loading.value = false
    }
  }

  async function signOut() {
    loading.value = true
    try {
      const { error } = await supabase.auth.signOut()
      if (error) throw error
      await navigateTo('/')
    }
    catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Erreur lors de la déconnexion'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
    }
    finally {
      loading.value = false
    }
  }

  async function resetPassword(email: string) {
    loading.value = true
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/confirm?type=recovery`
      })
      if (error) throw error
      toast.add({ title: 'Email envoyé', description: 'Vérifiez votre boîte mail pour réinitialiser votre mot de passe.', color: 'success' })
      return { success: true }
    }
    catch {
      // Always show success to not reveal if email exists (security)
      toast.add({ title: 'Email envoyé', description: 'Si ce compte existe, un email de réinitialisation a été envoyé.', color: 'success' })
      return { success: true }
    }
    finally {
      loading.value = false
    }
  }

  async function updatePassword(newPassword: string) {
    loading.value = true
    try {
      const { error } = await supabase.auth.updateUser({ password: newPassword })
      if (error) throw error
      toast.add({ title: 'Mot de passe mis à jour', color: 'success' })
      return { success: true }
    }
    catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Erreur lors de la mise à jour'
      toast.add({ title: 'Erreur', description: message, color: 'error' })
      return { success: false, error: message }
    }
    finally {
      loading.value = false
    }
  }

  return {
    user,
    loading,
    signUpWithEmail,
    signInWithEmail,
    signInWithGoogle,
    signOut,
    resetPassword,
    updatePassword
  }
}
