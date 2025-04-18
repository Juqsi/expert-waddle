<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.ts'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'


const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref<string | null>(null)

const handleSubmit = async () => {
  if (!email.value || !password.value) {
    errorMessage.value = "Credentials required"
    return
  }

  loading.value = true
  errorMessage.value = null

  await auth.login(email.value,password.value)
  loading.value = false
  router.push('/')
}
</script>

<template>
  <div class="flex items-center justify-center pt-12">
    <Card class="mx-auto max-w-sm w-full">
      <CardHeader>
        <CardTitle class="text-2xl">Login</CardTitle>
        <CardDescription>Demo? Ask for the 'testuser' credentials</CardDescription>
      </CardHeader>
      <CardContent>
        <form class="grid gap-4" @submit.prevent="handleSubmit">
          <div class="grid gap-2">
            <Label for="email">Username</Label>
            <Input id="email" v-model="email" placeholder="Type your username .." required />
          </div>
          <div class="grid gap-2">
            <div class="flex items-center">
              <Label for="password">Password</Label>
            </div>
            <Input id="password" v-model="password" required type="password" />
          </div>

          <Button :disabled="loading" class="w-full" type="submit">
            <span v-if="loading">Loading...</span>
            <span v-else>Sign In</span>
          </Button>
        </form>

      </CardContent>
    </Card>
  </div>
</template>
