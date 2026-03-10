<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950">
    <LayoutAppHeader />
    <div class="flex">
      <LayoutAppSidebar class="hidden lg:flex" />
      <main class="flex-1 p-6 lg:ml-64 max-w-7xl">
        <slot />
      </main>
    </div>
    <UNotifications />
  </div>
</template>
