import { ToggleButton } from './components/toggleButton';
import { useEffect } from 'react';
import ReactGA from 'react-ga4';
import { Outlet } from 'react-router-dom';

export function App() {


  useEffect(() => {

    const analytics = import.meta.env.VITE_GOOGLE_ANALYTICS_ID ?? false
    if (!analytics) return;

    ReactGA.initialize(analytics)
    ReactGA.send({ hitType: 'pageview', page: window.location.pathname })

  }, [window.location.pathname + window.location.search])


  return (

    <div className="w-auto h-screen relative">
      <ToggleButton />
      <Outlet />
    </div>

  )
}

