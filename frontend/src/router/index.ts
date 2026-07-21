import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('../views/LandingView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/registro',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/esqueci-senha',
      name: 'forgot-password',
      component: () => import('../views/auth/ForgotPasswordView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/redefinir-senha',
      name: 'reset-password',
      component: () => import('../views/auth/ResetPasswordView.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/oauth/callback',
      name: 'oauth-callback',
      component: () => import('../views/auth/OAuthCallbackView.vue'),
    },
    {
      path: '/app',
      component: () => import('../views/app/AppShellView.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', redirect: { name: 'app-home' } },
        {
          path: 'home',
          name: 'app-home',
          component: () => import('../views/app/AppHomeView.vue'),
        },
        {
          path: 'carteira',
          name: 'portfolio-home',
          component: () => import('../views/app/PortfolioView.vue'),
        },
        {
          path: 'mercado',
          name: 'market-home',
          component: () => import('../views/app/MarketView.vue'),
        },
        {
          path: 'mercado/:ticker',
          name: 'market-asset-detail',
          component: () => import('../views/app/AssetDetailView.vue'),
        },
        {
          path: 'aprendizado',
          name: 'glossary-home',
          component: () => import('../views/app/GlossaryView.vue'),
        },
        {
          path: 'simulacoes',
          name: 'simulations-home',
          component: () => import('../views/app/SimulationsView.vue'),
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'app-home' }
  }
})

export default router
