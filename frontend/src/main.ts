import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import i18n from './i18n'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(i18n)

const authStore = useAuthStore()
authStore.tryRestoreSession().finally(() => {
  app.use(router)
  app.mount('#app')
})
