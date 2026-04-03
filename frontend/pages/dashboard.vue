<script setup lang="ts">
import type { Job } from '~/types'

definePageMeta({ middleware: 'auth' })

const { push } = useToast()
const { downloadResultFile } = useFileDownload()

const jobs = ref<Job[]>([])
const loadingJobs = ref(false)
const uploadLoading = ref(false)
const selectedFile = ref<File | null>(null)
const downloadingJobId = ref<string | null>(null)

const options = reactive({
  output_format: 'png',
  resize_width: null as number | null,
  resize_height: null as number | null,
  crop_x: null as number | null,
  crop_y: null as number | null,
  crop_width: null as number | null,
  crop_height: null as number | null,
  fit_width: null as number | null,
  fit_height: null as number | null,
})

const selectFile = (file: File) => {
  selectedFile.value = file
}

const fetchJobs = async () => {
  loadingJobs.value = true
  try {
    jobs.value = await useApi<Job[]>('/api/v1/jobs?limit=10')
  } catch (e) {
    push(e instanceof Error ? e.message : 'Could not load jobs', 'error')
  } finally {
    loadingJobs.value = false
  }
}

const submit = async () => {
  if (!selectedFile.value) {
    push('Please choose a file first', 'info')
    return
  }

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('output_format', options.output_format)

  if (options.resize_width) formData.append('resize_width', String(options.resize_width))
  if (options.resize_height) formData.append('resize_height', String(options.resize_height))
  if (options.crop_x !== null) formData.append('crop_x', String(options.crop_x))
  if (options.crop_y !== null) formData.append('crop_y', String(options.crop_y))
  if (options.crop_width) formData.append('crop_width', String(options.crop_width))
  if (options.crop_height) formData.append('crop_height', String(options.crop_height))
  if (options.fit_width) formData.append('fit_width', String(options.fit_width))
  if (options.fit_height) formData.append('fit_height', String(options.fit_height))

  uploadLoading.value = true
  try {
    await useApi<Job>('/api/v1/jobs/remove-background', {
      method: 'POST',
      body: formData,
    })
    push('Job queued successfully', 'success')
    selectedFile.value = null
    await fetchJobs()
  } catch (e) {
    push(e instanceof Error ? e.message : 'Upload failed', 'error')
  } finally {
    uploadLoading.value = false
  }
}

const downloadResult = async (job: Job) => {
  downloadingJobId.value = job.id
  try {
    await downloadResultFile(job)
  } catch (e) {
    push(e instanceof Error ? e.message : 'Download failed', 'error')
  } finally {
    downloadingJobId.value = null
  }
}

let pollTimer: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  await fetchJobs()
  pollTimer = setInterval(fetchJobs, 4000)
})

onBeforeUnmount(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<template>
  <div class="grid gap-6 lg:grid-cols-[1.1fr,0.9fr]">
    <section class="card p-6">
      <h1 class="text-2xl font-extrabold">New Background Removal</h1>
      <p class="mt-2 text-sm text-slate-500">Upload image, tweak output, queue processing job.</p>

      <div class="mt-6 space-y-4">
        <UploadDropzone @file-selected="selectFile" />
        <p v-if="selectedFile" class="text-sm font-medium text-slate-700">Selected: {{ selectedFile.name }}</p>

        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Output format</label>
            <select v-model="options.output_format" class="input-base">
              <option value="png">PNG</option>
              <option value="jpeg">JPEG</option>
              <option value="webp">WEBP</option>
            </select>
          </div>
          <div />
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Resize width</label>
            <input v-model.number="options.resize_width" class="input-base" type="number" min="1" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Resize height</label>
            <input v-model.number="options.resize_height" class="input-base" type="number" min="1" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Crop X</label>
            <input v-model.number="options.crop_x" class="input-base" type="number" min="0" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Crop Y</label>
            <input v-model.number="options.crop_y" class="input-base" type="number" min="0" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Crop width</label>
            <input v-model.number="options.crop_width" class="input-base" type="number" min="1" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Crop height</label>
            <input v-model.number="options.crop_height" class="input-base" type="number" min="1" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Fit width</label>
            <input v-model.number="options.fit_width" class="input-base" type="number" min="1" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-semibold text-slate-700">Fit height</label>
            <input v-model.number="options.fit_height" class="input-base" type="number" min="1" />
          </div>
        </div>

        <button class="btn-primary" :disabled="uploadLoading" @click="submit">
          {{ uploadLoading ? 'Queueing...' : 'Queue job' }}
        </button>
      </div>
    </section>

    <section class="card p-6">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-bold">Recent Jobs</h2>
        <NuxtLink class="text-sm font-semibold text-brand-700" to="/jobs">View all</NuxtLink>
      </div>

      <div v-if="loadingJobs" class="mt-4 text-sm text-slate-500">Loading jobs...</div>
      <div v-else-if="jobs.length === 0" class="mt-4 text-sm text-slate-500">No jobs yet.</div>

      <div v-else class="mt-4 space-y-3">
        <article v-for="job in jobs" :key="job.id" class="rounded-xl border border-slate-200 bg-slate-50 p-3">
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="text-sm font-semibold text-slate-700">{{ job.id }}</p>
              <p class="text-xs text-slate-500">{{ new Date(job.created_at).toLocaleString() }}</p>
            </div>
            <JobStatusBadge :status="job.status" />
          </div>

          <div v-if="job.result_url" class="mt-3">
            <button
              class="btn-secondary inline-flex"
              :disabled="downloadingJobId === job.id"
              @click="downloadResult(job)"
            >
              {{ downloadingJobId === job.id ? 'Downloading...' : 'Download result' }}
            </button>
          </div>

          <p v-if="job.error_message" class="mt-2 text-xs font-medium text-rose-600">{{ job.error_message }}</p>
        </article>
      </div>
    </section>
  </div>
</template>
