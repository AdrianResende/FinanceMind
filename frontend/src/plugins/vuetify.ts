import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#0F4C64',
          'primary-darken-1': '#0A3A4D',
          secondary: '#0E9C8F',
          'secondary-darken-1': '#0B7A70',
          success: '#1B8A5A',
          error: '#D64545',
          warning: '#C77D18',
          info: '#2A7DE1',
          background: '#F7F9FA',
          surface: '#FFFFFF',
        },
      },
    },
  },
})
