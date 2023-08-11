import { Link, Navigate, useParams, useSearchParams } from "react-router-dom";
import { PiAirplaneInFlightFill } from "react-icons/pi";
import { 
  Stack,
  Typography,
  Paper
} from '@mui/material'

import { useFlightDetails } from "../hooks/useFlightDetail";
import { Calendar } from "../components/analytics/calendar";
import { Spinner } from "../components/spinner";
import { Combo } from "../components/analytics/combo";


export const AnalyticsView = () => {

  const [searchParams] = useSearchParams();
  const origin = searchParams.get('origin');
  const destination = searchParams.get('destination');


  if (!origin || !destination) {
    return <Navigate to="/" />
  }

  const { data, isLoading, isError } = useFlightDetails({origin, destination})


  if (isError) return <div>Error...</div>

  if (isLoading || !data) return <Spinner />


  return (
    <Stack>
      <Stack
        p={2}
      >
        <Typography 
          variant="h3"
          className="italic"
        >
          <Link to='/'>
            Milleros
          </Link>
        </Typography>
      </Stack>
      <section>
        <Stack 
          direction="row"
          gap={2}
          alignItems="center"
          justifyContent="center"
        >
          <Paper 
            sx={{
              p: 2,
            }}
          >
            {data.origin}
          </Paper>
          <PiAirplaneInFlightFill className="w-7 h-7"/>
          <Paper 
            sx={{
              p: 2,
            }}
            // className='text-lg font-semibold dark:bg-orange-500 bg-zinc-600 p-3 px-5 rounded-md text-neutral-100'
          >
            {data.dest}
          </Paper>
        </Stack>
      </section>

      <Calendar data={data!} />
      <Combo origin={origin} destination={destination} />

    </Stack>
  )
}
