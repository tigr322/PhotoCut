<script setup lang="ts">
import type { Job } from '~/types'

definePageMeta({ middleware: 'auth' })

const { push } = useToast()
const config = useRuntimeConfig()

const jobs = ref<Job[]>([])
const loading = ref(false)

const load = async () => {
  loading.value = true
  try {
    jobs.value = await useApi<Job[]>('/api/v1/jobs?limit=100')
  } catch (e) {
    push(e instanceof Error ? e.message : 'Failed to load jobs', 'error')
  } finally {
    loading.value = false
  }
}

let pollTimer: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  await load()
  pollTimer = setInterval(load, 4000)
})

onBeforeUnmount(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<template>
  <section class="card p-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-extrabold">Jobs</h1>
      <button class="btn-secondary" @click="load">Refresh</button>
    </div>

    <div v-if="loading" class="mt-4 text-sm text-slate-500">Loading...</div>
    <div v-else-if="jobs.length === 0" class="mt-4 text-sm text-slate-500">No jobs found.</div>

    <div v-else class="mt-4 overflow-x-auto">
      <table class="min-w-full divide-y divide-slate-200 text-sm">
        <thead>
          <tr class="text-left text-slate-500">
            <th class="py-2 pr-4 font-semibold">ID</th>
            <th class="py-2 pr-4 font-semibold">Status</th>
            <th class="py-2 pr-4 font-semibold">Created</th>
            <th class="py-2 pr-4 font-semibold">Result</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="job in jobs" :key="job.id">
            <td class="py-3 pr-4 font-medium text-slate-700">{{ job.id }}</td>
            <td class="py-3 pr-4"><JobStatusBadge :status="job.status" /></td>
            <td class="py-3 pr-4 text-slate-500">{{ new Date(job.created_at).toLocaleString() }}</td>
            <td class="py-3 pr-4">
              <a
                v-if="job.result_url"
                :href="`${config.public.apiBase}${job.result_url}`"
                target="_blank"
                rel="noopener"
                class="text-brand-700 hover:underline"
              >
                Download
              </a>
              <span v-else class="text-slate-400">-</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
