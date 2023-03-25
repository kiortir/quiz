import App from './App'
import React from 'react'
import ReactDOM from 'react-dom/client'

import { MantineProvider } from '@mantine/core'
import { Notifications } from '@mantine/notifications'

import '@fontsource/inter'
import '@fontsource/montserrat'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <MantineProvider
      theme={{
          colorScheme: 'dark',
          fontFamily: 'Inter',
          breakpoints: {
            xs: '30em',
            sm: '48em',
            md: '64em',
            lg: '74em',
            xl: '90em',
          },
          headings: {
            fontFamily: 'Montserrat',
          },
      }}
      withGlobalStyles
      withNormalizeCSS
    >
      <Notifications />
      <App />
    </MantineProvider>
  </React.StrictMode>,
)
