export function useDarkMode() {
  const isDark = useState<boolean>('darkMode', () => false)

  function init() {
    if (import.meta.server) return
    const stored = localStorage.getItem('ats-theme')
    isDark.value = stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)
    applyClass()
  }

  function toggle() {
    isDark.value = !isDark.value
    localStorage.setItem('ats-theme', isDark.value ? 'dark' : 'light')
    applyClass()
  }

  function applyClass() {
    document.documentElement.classList.toggle('dark', isDark.value)
  }

  return { isDark, init, toggle }
}
