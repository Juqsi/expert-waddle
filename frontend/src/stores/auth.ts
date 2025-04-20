import { defineStore } from 'pinia'
import router from '@/router'
import {toast} from "vue-sonner";

export const BASE_PATH = import.meta.env.VITE_API_BASE || ''

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAdmin: true,
    token: null as string | null,
    isAuthenticated: true
  }),
  actions: {
    async login(username: string, password: string) {
      try {
        const response = await fetch(`${BASE_PATH}/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        })

        if (!response.ok) {
          console.error('Login failed:', response.statusText)
          toast.error('Login failed: ' + response.statusText)
          this.token = null
          this.isAuthenticated = false
          this.isAdmin = false
          return false
        }

        const data = await response.json()
        this.token = data.token
        this.isAdmin = data.admin
        this.isAuthenticated = true
        toast.success('Login successfully')
        return true
      } catch (error) {
        console.error('Login error:', error)
        toast.error('Login failed: ' + error)
        this.token = null
        this.isAuthenticated = false
        this.isAdmin = false
        return false
      }
    },
    logout() {
      this.token = null
      this.isAuthenticated = false
      this.isAdmin = false
      router.push('/login')
    },
  },
  persist: {
    storage: localStorage,
  },
})
