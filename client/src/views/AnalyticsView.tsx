import { Navigate, useParams, useSearchParams } from "react-router-dom";
import { PiAirplaneInFlightFill } from "react-icons/pi";
import { Chart, ChartWrapperOptions } from 'react-google-charts';

import { useFlightDetails } from "../hooks/useFlightDetail";
import { useMemo } from "react";


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

  const calendarData = [
    [
      { type: "date", id: "Date" },
      { type: "number", id: "Won/Loss" },
    ],
    [new Date(2022, 3, 13), 37032],
    ...data.details.map(
      detail => [new Date(detail.flight_date), detail.miles]
    )
  ];


  const options: ChartWrapperOptions['options'] = {
    
  }



  return (
    <main className='mx-auto dark:text-neutral-100 py-5 flex justify-center flex-col'>
        <div className='h-[35%] w-screen bg-neutral-100 dark:bg-neutral-800'>
          <h1 className="flex flex-col justify-end p-10 items-center h-full">
            Milleros
          </h1>
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
      <section className="flex justify-center h-full border mt-5 p-5 overflow-auto min-w-[950px]">
        <Chart
          chartType="Calendar"
          width="950px"
          height="400px"
          data={calendarData}
          options={options}
        />
      </section>

    </main>
  )
}
