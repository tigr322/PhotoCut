<script setup lang="ts">
import type { ApiKeyCreateResponse, ApiKeyRecord } from '~/types'

definePageMeta({ middleware: 'auth' })

const { push } = useToast()

const keys = ref<ApiKeyRecord[]>([])
const loading = ref(false)
const creating = ref(false)
const newKeyName = ref('Default API Key')
const revealedKey = ref<ApiKeyCreateResponse | null>(null)

const load = async () => {
  loading.value = true
  try {
    keys.value = await useApi<ApiKeyRecord[]>('/api/v1/api-keys')
  } catch (e) {
    push(e instanceof Error ? e.message : 'Failed to load API keys', 'error')
  } finally {
    loading.value = false
  }
}

const createKey = async () => {
  creating.value = true
  try {
    revealedKey.value = await useApi<ApiKeyCreateResponse>('/api/v1/api-keys', {
      method: 'POST',
      body: { name: newKeyName.value },
    })
    push('API key created. Save it now.', 'success')
    await load()
  } catch (e) {
    push(e instanceof Error ? e.message : 'Failed to create API key', 'error')
  } finally {
    creating.value = false
  }
}

const revokeKey = async (id: string) => {
  try {
    await useApi(`/api/v1/api-keys/${id}`, { method: 'DELETE' })
    push('API key revoked', 'success')
    await load()
  } catch (e) {
    push(e instanceof Error ? e.message : 'Failed to revoke key', 'error')
  }
}

onMounted(load)
</script>

<template>
  <section class="grid gap-6 lg:grid-cols-[1fr,1fr]">
    <div class="card p-6">
      <h1 class="text-2xl font-extrabold">API Keys</h1>
      <p class="mt-2 text-sm text-slate-500">Create keys for server-to-server API integrations.</p>

      <div class="mt-5 space-y-3">
        <div>
          <label class="mb-1 block text-sm font-semibold text-slate-700">Key name</label>
          <input v-model="newKeyName" class="input-base" type="text" />
        </div>
        <button class="btn-primary" :disabled="creating" @click="createKey">{{ creating ? 'Creating...' : 'Create key' }}</button>
      </div>

      <div v-if="revealedKey" class="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-4">
        <p class="text-sm font-bold text-amber-800">Copy this key now. It will not be shown again.</p>
        <code class="mt-2 block break-all rounded-lg bg-white p-3 text-xs text-slate-800">{{ revealedKey.key }}</code>
      </div>
    </div>

    <div class="card p-6">
      <h2 class="text-xl font-bold">Existing Keys</h2>
      <p v-if="loading" class="mt-3 text-sm text-slate-500">Loading...</p>
      <p v-else-if="keys.length === 0" class="mt-3 text-sm text-slate-500">No API keys yet.</p>

      <div v-else class="mt-4 space-y-3">
        <article v-for="key in keys" :key="key.id" class="rounded-xl border border-slate-200 p-4">
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="font-semibold text-slate-800">{{ key.name }}</p>
              <p class="text-xs text-slate-500">Prefix: {{ key.key_prefix }}</p>
              <p class="text-xs text-slate-500">Created: {{ new Date(key.created_at).toLocaleString() }}</p>
            </div>

            <button class="btn-secondary" :disabled="Boolean(key.revoked_at)" @click="revokeKey(key.id)">
              {{ key.revoked_at ? 'Revoked' : 'Revoke' }}
            </button>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
