import { Link, Navigate, useParams, useSearchParams } from "react-router-dom";
import { PiAirplaneInFlightFill } from "react-icons/pi";

import { useFlightDetails } from "../hooks/useFlightDetail";
import { Calendar } from "../components/analytics/calendar";


export const AnalyticsView = () => {

  const [searchParams] = useSearchParams();
  const origin = searchParams.get('origin');
  const destination = searchParams.get('destination');


  if (!origin || !destination) {
    return <Navigate to="/" />
  }

  const { data, isLoading, isError } = useFlightDetails({origin, destination})


  if (isError) return <div>Error...</div>

  if (isLoading || !data) return <div>Loading...</div>



  return (
    <main className='mx-auto dark:text-neutral-100 py-5 flex justify-center flex-col'>
        <div className="bg-neutral-100 dark:bg-neutral-800 flex flex-col p-5 justify-center dark:text-neutral-300 text-neutral-800">
          <Link to='/'>
            <h1 className="md:text-5xl text-4xl font-bold italic">Milleros</h1>
          </Link>
        </div>
      <section>
        <div className="flex gap-4 sm:gap-5 justify-center p-5 items-center sm:flex-row flex-col">
          <p 
            className='text-lg font-semibold dark:bg-orange-500 bg-zinc-600 p-3 px-5 rounded-md text-neutral-100'
          >
            {data.origin}
          </p>
          <PiAirplaneInFlightFill className="w-7 h-7"/>
          <p 
            className='text-lg font-semibold dark:bg-orange-500 bg-zinc-600 p-3 px-5 rounded-md text-neutral-100'
          >
            {data.dest}
          </p>
        </div>
      </section>

      <Calendar data={data!} />

    </main>
  )
}
