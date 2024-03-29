import { Link, Navigate, useSearchParams } from "react-router-dom";
import { PiAirplaneInFlightFill } from "react-icons/pi";
import { 
  Stack,
  Link as MLink,
  Typography,
  Paper,
  Container,
  Alert,
} from '@mui/material'

import { useFlightDetails } from "../hooks/useFlightDetail";
import { Spinner } from "../components/spinner";
import { FlightsTable } from "../components/analytics/table";
import { HeatMap } from "../components/analytics/heatmap";
import { ColumnBar } from "../components/analytics/column-bar";

import logo from '../assets/logo.png'


export const AnalyticsView = () => {

  const [searchParams] = useSearchParams();
  const origin = searchParams.get('origin');
  const destination = searchParams.get('destination');

  if (!origin || !destination) {
    return <Navigate to="/" />
  }

  const { data, isLoading, isError } = useFlightDetails({origin, destination})

  if (isError) return (
    <Stack
      justifyContent="center"
      alignItems="center"
      height="100vh"
    >
      <Alert severity="error">
        Error al cargar los datos. 
        <MLink 
          sx={{ ml: 1 }}
          href='/' 
          underline='always'
          color='inherit'
        >
          Volver al inicio
        </MLink>
      </Alert>
    </Stack>

  )

  if (isLoading || !data) return <Spinner />


  return (
    <Container maxWidth="xl">
      <Stack p={2}  >
        <Link to='/'>
          <Stack flexDirection="row" gap={1} alignItems="center">
            <img src={logo} className="w-16 h-16"/>
            <Typography 
              variant="h3"
              className="italic"
              color="grey.300"
            >
              Milleros
            </Typography>
          </Stack>
        </Link>
      </Stack>
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
          <Typography textAlign='center'>
            {data.origin}
          </Typography>
        </Paper>
        <PiAirplaneInFlightFill className="w-7 h-7"/>
        <Paper 
          sx={{
            p: 2,
          }}
        >
          <Typography textAlign='center'>
            {data.dest}
          </Typography>
        </Paper>
      </Stack>

      <Stack
        my={5}
      >
        <FlightsTable data={{ ...data, details: data.details.filter(d => new Date(d.flight_date) > new Date() ) }}/>
        <HeatMap data={data}/>
        <ColumnBar origin={origin} destination={destination} />
      </Stack>


    </Container>
  )
}
