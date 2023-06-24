import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { RouterProvider } from 'react-router-dom'
import { router } from './router'
import { CssBaseline, ThemeProvider } from '@mui/material'
import theme from './theme'
import { QueryClient, QueryClientProvider } from 'react-query'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={ theme }>
        <CssBaseline />
        <RouterProvider router={ router } />
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>,
)
