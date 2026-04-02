<script setup lang="ts">
const auth = useAuthStore()
auth.init()

if (auth.isAuthenticated) {
  await navigateTo('/dashboard')
} else {
  await navigateTo('/login')
}
</script>

<template>
  <div />
</template>
