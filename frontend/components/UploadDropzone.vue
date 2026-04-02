<script setup lang="ts">
const emit = defineEmits<{ (e: 'file-selected', file: File): void }>()

const dragActive = ref(false)

const onDrop = (event: DragEvent) => {
  event.preventDefault()
  dragActive.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    emit('file-selected', file)
  }
}

const onInputChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    emit('file-selected', file)
  }
}
</script>

<template>
  <label
    class="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 p-8 text-center transition"
    :class="dragActive ? 'border-brand-500 bg-brand-50' : 'bg-white hover:border-brand-400'"
    @dragover.prevent="dragActive = true"
    @dragleave.prevent="dragActive = false"
    @drop="onDrop"
  >
    <input class="hidden" type="file" accept="image/png,image/jpeg,image/webp" @change="onInputChange" />
    <p class="text-lg font-bold text-slate-800">Drop an image here</p>
    <p class="mt-1 text-sm text-slate-500">PNG, JPG, WEBP up to backend limit</p>
    <p class="mt-4 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">or click to choose</p>
  </label>
</template>
