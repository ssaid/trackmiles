import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { RouterProvider } from 'react-router-dom'
import { router } from './router'
import { QueryClient, QueryClientProvider } from 'react-query'

import { ColorModeProvider } from './context/theme';

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ColorModeProvider>
        <RouterProvider router={ router } />
      </ColorModeProvider>
    </QueryClientProvider>
  </React.StrictMode>,
)
