<script setup lang="ts">
const { toasts } = useToast()

const getStyle = (type: string) => {
  if (type === 'success') return 'border-emerald-200 bg-emerald-50 text-emerald-800'
  if (type === 'error') return 'border-rose-200 bg-rose-50 text-rose-800'
  return 'border-slate-200 bg-white text-slate-800'
}
</script>

<template>
  <div class="fixed right-4 top-4 z-50 flex w-80 flex-col gap-2">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="rounded-xl border px-4 py-3 text-sm font-medium shadow-soft"
      :class="getStyle(toast.type)"
    >
      {{ toast.message }}
    </div>
  </div>
</template>
