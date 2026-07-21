import type { GlobalThemeOverrides } from 'naive-ui'

export const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#0F4C64',
    primaryColorHover: '#0A3A4D',
    primaryColorPressed: '#082C3B',
    primaryColorSuppl: '#0F4C64',
    infoColor: '#2A7DE1',
    infoColorHover: '#1E6BC9',
    infoColorPressed: '#1857A3',
    successColor: '#1B8A5A',
    successColorHover: '#166F49',
    successColorPressed: '#125A3B',
    errorColor: '#D64545',
    errorColorHover: '#C13333',
    errorColorPressed: '#A62A2A',
    warningColor: '#C77D18',
    warningColorHover: '#AD6B12',
    warningColorPressed: '#93590F',
    borderRadius: '14px',
    borderRadiusSmall: '10px',
    fontFamily:
      "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif",
  },
  Card: {
    borderRadius: '20px',
  },
  Button: {
    borderRadiusMedium: '10px',
    borderRadiusLarge: '12px',
    fontWeightStrong: '600',
  },
}
