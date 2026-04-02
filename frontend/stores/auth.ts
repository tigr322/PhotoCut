import { defineStore } from 'pinia'
import type { TokenResponse, User } from '~/types'

interface AuthState {
  token: string | null
  user: User | null
  initialized: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: null,
    user: null,
    initialized: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    init() {
      if (!process.client || this.initialized) {
        return
      }

      const token = localStorage.getItem('photocut_token')
      const userRaw = localStorage.getItem('photocut_user')

      this.token = token
      this.user = userRaw ? (JSON.parse(userRaw) as User) : null
      this.initialized = true
    },

    persist() {
      if (!process.client) {
        return
      }

      if (this.token) {
        localStorage.setItem('photocut_token', this.token)
      } else {
        localStorage.removeItem('photocut_token')
      }

      if (this.user) {
        localStorage.setItem('photocut_user', JSON.stringify(this.user))
      } else {
        localStorage.removeItem('photocut_user')
      }
    },

    async login(email: string, password: string) {
      const config = useRuntimeConfig()
      const response = await $fetch<TokenResponse>('/api/v1/auth/login', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { email, password },
      })

      this.token = response.access_token
      this.user = response.user
      this.persist()
    },

    async register(email: string, password: string) {
      const config = useRuntimeConfig()
      await $fetch('/api/v1/auth/register', {
        baseURL: config.public.apiBase,
        method: 'POST',
        body: { email, password },
      })
    },

    async fetchProfile() {
      if (!this.token) {
        return
      }
      const config = useRuntimeConfig()
      const user = await $fetch<User>('/api/v1/me', {
        baseURL: config.public.apiBase,
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      })
      this.user = user
      this.persist()
    },

    logout() {
      this.token = null
      this.user = null
      this.persist()
    },
  },
})
