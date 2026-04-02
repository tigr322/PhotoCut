<script setup lang="ts">
import type { JobStatus } from '~/types'

defineProps<{ status: JobStatus }>()

const classes: Record<JobStatus, string> = {
  pending: 'bg-slate-100 text-slate-700',
  queued: 'bg-amber-100 text-amber-700',
  processing: 'bg-sky-100 text-sky-700',
  completed: 'bg-emerald-100 text-emerald-700',
  failed: 'bg-rose-100 text-rose-700',
}
</script>

<template>
  <span class="rounded-full px-2.5 py-1 text-xs font-bold" :class="classes[status]">{{ status }}</span>
</template>
