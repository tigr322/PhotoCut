<script setup lang="ts">
definePageMeta({ middleware: 'guest' })

const auth = useAuthStore()
const { push } = useToast()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  try {
    await auth.register(email.value, password.value)
    push('Account created. Please sign in.', 'success')
    await navigateTo('/login')
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-md">
    <div class="card p-8">
      <h1 class="text-2xl font-extrabold">Create account</h1>
      <p class="mt-2 text-sm text-slate-500">Start processing images in minutes.</p>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Email</label>
          <input v-model="email" class="input-base" type="email" required autocomplete="email" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Password</label>
          <input v-model="password" class="input-base" type="password" required minlength="8" autocomplete="new-password" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Confirm password</label>
          <input
            v-model="confirmPassword"
            class="input-base"
            type="password"
            required
            minlength="8"
            autocomplete="new-password"
          />
        </div>

        <p v-if="error" class="text-sm font-medium text-rose-600">{{ error }}</p>

        <button class="btn-primary w-full" :disabled="loading">{{ loading ? 'Creating...' : 'Create account' }}</button>
      </form>

      <p class="mt-4 text-sm text-slate-600">
        Already registered?
        <NuxtLink class="font-semibold text-brand-700" to="/login">Sign in</NuxtLink>
      </p>
    </div>
  </section>
</template>
