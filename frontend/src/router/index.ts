import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import {useAuthStore} from "@/stores/auth.ts";
import LoginView from "@/views/LoginView.vue";
import AdminView from "@/views/AdminView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {requiresAuth: true, requiresAdmin: false},
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {requiresAuth: false, requiresAdmin: false},
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminView,
      meta: {requiresAuth: false, requiresAdmin: true},
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
      meta: {requiresAuth: true, requiresAdmin: false},
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/UploadPhotoView.vue'),
      meta: {requiresAuth: true, requiresAdmin: false},
    },
    {
      path: '/last/:number',
      name: 'Plant',
      component: () => import('@/views/PlantInformationView.vue'),
      meta: {requiresAuth: true, requiresAdmin: false},
    },
    {
      path: '/search',
      name: 'SearchPlant',
      component: () => import('@/views/SearchPlantView.vue'),
      meta: {requiresAuth: true, requiresAdmin: false},
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/404View.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAdmin && !authStore.isAdmin){
    next({name: 'login', query: {redirect: to.fullPath.startsWith('/') ? to.fullPath : '/'}})
  } else if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({name: 'login', query: {redirect: to.fullPath.startsWith('/') ? to.fullPath : '/'}})
  } else if (to.meta.requiresUnauth && authStore.isAuthenticated) {
    next({name: 'home'})
  } else {
    next()
  }
})

export default router
