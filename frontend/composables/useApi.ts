import type { FetchOptions } from 'ofetch'
import { FetchError } from 'ofetch'

export const useApi = async <T>(path: string, options: FetchOptions<'json'> = {}) => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  const headers = new Headers(options.headers as HeadersInit | undefined)
  if (auth.token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${auth.token}`)
  }

  try {
    return await $fetch<T>(path, {
      ...options,
      baseURL: config.public.apiBase,
      headers,
    })
  } catch (error) {
    if (error instanceof FetchError) {
      if (error.status === 401) {
        auth.logout()
      }
      const detail = (error.data as { detail?: string } | undefined)?.detail
      throw new Error(detail || error.message)
    }
    throw error
  }
}
