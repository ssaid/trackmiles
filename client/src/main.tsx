import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { 
  QueryClient, 
  QueryClientProvider 
} from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

import { RouterProvider } from 'react-router-dom'
import { router } from './router'

import { ColorModeProvider } from './context/theme';

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ColorModeProvider>
        <RouterProvider router={ router } />
      </ColorModeProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>,
)
