import { ToggleButton } from './components/toggleButton';
import { useEffect } from 'react';
import ReactGA from 'react-ga4';
import { Outlet } from 'react-router-dom';
import { Stack } from '@mui/system';
import { Container } from '@mui/material';

export function App() {


  useEffect(() => {

    const analytics = import.meta.env.VITE_GOOGLE_ANALYTICS_ID ?? false
    if (!analytics) return;

    ReactGA.initialize(analytics)
    ReactGA.send({ hitType: 'pageview', page: window.location.pathname })

  }, [window.location.pathname + window.location.search])


  return (
    <Stack>
      <ToggleButton />
      <Container maxWidth='xl'>
        <Outlet />
      </Container>
    </Stack>

  )
}

