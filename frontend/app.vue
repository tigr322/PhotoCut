<script setup lang="ts">
const auth = useAuthStore()
auth.init()
</script>

<template>
  <div class="min-h-screen">
    <ToastStack />
    <header class="border-b border-slate-200 bg-white/90 backdrop-blur">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <NuxtLink to="/dashboard" class="text-xl font-extrabold text-slate-900">PhotoCut</NuxtLink>

        <nav v-if="auth.isAuthenticated" class="flex items-center gap-2 text-sm font-semibold">
          <NuxtLink class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-100" to="/dashboard">Dashboard</NuxtLink>
          <NuxtLink class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-100" to="/jobs">Jobs</NuxtLink>
          <NuxtLink class="rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-100" to="/api-keys">API Keys</NuxtLink>
          <button class="rounded-lg bg-slate-900 px-3 py-2 text-white" @click="auth.logout(); navigateTo('/login')">Logout</button>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8">
      <NuxtPage />
    </main>
  </div>
</template>
