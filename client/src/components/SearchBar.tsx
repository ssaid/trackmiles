import { Autocomplete, Box, Button, Paper, Skeleton, Stack, TextField } from "@mui/material"
import { useCallback, useMemo, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAirports } from "../hooks/useAirports"


export const SearchBar = () => {

  const { airports } = useAirports()
  const navigate = useNavigate();

  const { data, error, isLoading } = airports

  const [ origin, setOrigin ] = useState<string | null>(null)
  const [ destination, setDestination ] = useState<string | null>(null)

  const origins = useMemo(
    () => data?.map(({airport_origin}) => airport_origin.display_name)
  , [data])

  const getDestinations = useCallback((origin: string | null) => {
    return data
      ?.find(ap => ap.airport_origin.display_name === origin)
      ?.airport_destinations?.map(dest => dest.display_name) ?? []

  }, [data])

  const handleOriginChange = (_: any, newValue: string) => {
    if (!getDestinations(newValue).includes(destination!)) setDestination(null)
    setOrigin(newValue)
  }

  const getAirportCode = (airportName: string) => {

      const airports = data?.flatMap(x => [x.airport_origin, ...x.airport_destinations])

      return airports!.find(x => x.display_name === airportName)?.code ?? ''
  }


  const handleSubmit = () => {
    const params = new URLSearchParams()
    params.append('origin', getAirportCode(origin!))
    params.append('destination', getAirportCode(destination!))

    navigate(`/analytics?${params.toString()}`)

  }


  if (isLoading) return (

    <div 
      className="flex flex-col lg:w-[90%] w-[95%] md:flex-row justify-center align-center gap-3 bg-neutral-100 dark:bg-neutral-800 p-8 rounded border-2 border-zinc-200 dark:border-zinc-700"
    >
      <Skeleton variant="rounded" animation="wave" >
        <TextField sx={{ minWidth: 300 }} />
      </Skeleton>
      <Skeleton variant="rounded" animation="wave" >
        <TextField sx={{ minWidth: 300 }} />
      </Skeleton>
      <Skeleton variant="rounded" animation="wave" >
        <button className="rounded p-2 px-4">Buscar</button>
      </Skeleton>


    </div>
  )


  return (
    <Box
      display="flex"
      justifyContent="center"
      height='150px'
      width='100%'
      position="relative"
    >
      <Box
        top={-10}
        position="absolute"
        height='200px'
        width='100%'
        bgcolor='background.paper'
        sx={{
          transform: 'skew(0deg, -2deg);',
        }}
      ></Box>
      <Paper
        sx={{
          p: 2,
          position: 'relative',
          height:'fit-content',
          top: -40,
          minWidth: { xs: '90%', lg: 900 },
        }}
      >
        <Stack
          alignItems='center'
          gap={2}
          // flexWrap= 'wrap'
          direction={{ xs: 'column', sm: 'row' }}
        >
          <Autocomplete
            disablePortal
            isOptionEqualToValue={(option, value) => option === value}
            options={origins!}
            fullWidth
            // sx={{ minWidth: 250, width: '100%' }}
            onInputChange={handleOriginChange}
            value={origin}
            renderInput={(params) => 
              <TextField 
                {...params} 
                label="Origen" 
              />
            }
          />
          <Autocomplete
            disablePortal
            options={getDestinations(origin)}
            isOptionEqualToValue={(option, value) => option === value}
            value={destination}
            onChange={(_, newValue) => setDestination(newValue)}
            fullWidth
            // sx={{ width: '100%' }}
            renderInput={(params) => <TextField {...params} label="Destino" />}
          />


          <Button
            disabled={!origin || !destination}
            onClick={handleSubmit}
            variant="contained"
            sx={{ 
              height: 55,
              width: { xs: '100%', sm: 'fit-content'},
              minWidth: 100,
            }}

          >
            Buscar
          </Button>
        </Stack>
      </Paper>
    </Box>
  )
}
