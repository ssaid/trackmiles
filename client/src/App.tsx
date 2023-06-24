import { useEffect } from 'react';
import ReactGA from 'react-ga4';
import { Outlet } from 'react-router-dom';
import bgImage from './assets/bg.jpg'
import { Wave } from './components/Wave';

export function App() {


  useEffect(() => {

    const analytics = import.meta.env.VITE_GOOGLE_ANALYTICS_ID ?? false
    if (!analytics) return;

    ReactGA.initialize(analytics)
    ReactGA.send({ hitType: 'pageview', page: window.location.pathname })

  }, [window.location.pathname + window.location.search])


  return (

    <div className="w-auto h-screen relative">

      <div>
        <div className="absolute inset-0">
          <img 
            src={bgImage} 
            alt="background" 
            className="absolute object-cover w-full h-full -z-10"
          />
          <div className="absolute inset-0 bg-black opacity-60"></div>
        </div>

        <div className="absolute h-screen w-screen flex flex-col justify-end object-fill">
          <Wave/>
          <div className='h-[35%] w-screen bg-neutral-100'>
            <div className="flex flex-col justify-end p-10 items-center h-full">
              Milleros
            </div>
          </div>
        </div>


        
      </div>
      <Outlet />
    </div>

  )
}

