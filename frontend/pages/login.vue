<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const auth = useAuthStore()
const { push } = useToast()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    push('Welcome back', 'success')
    await navigateTo('/dashboard')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-md">
    <div class="card p-8">
      <h1 class="text-2xl font-extrabold">Sign in</h1>
      <p class="mt-2 text-sm text-slate-500">Manage jobs, files, and API keys.</p>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Email</label>
          <input v-model="email" class="input-base" type="email" required autocomplete="email" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Password</label>
          <input v-model="password" class="input-base" type="password" required autocomplete="current-password" />
        </div>

        <p v-if="error" class="text-sm font-medium text-rose-600">{{ error }}</p>

        <button class="btn-primary w-full" :disabled="loading">{{ loading ? 'Signing in...' : 'Sign in' }}</button>
      </form>

      <p class="mt-4 text-sm text-slate-600">
        No account?
        <NuxtLink class="font-semibold text-brand-700" to="/register">Create one</NuxtLink>
      </p>
    </div>
  </section>
</template>
