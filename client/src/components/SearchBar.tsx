import { Autocomplete, Skeleton, Stack, TextField } from "@mui/material"
import { useCallback, useMemo, useState } from "react"
import { PiAirplaneInFlightFill } from "react-icons/pi"
import { Link, useNavigate } from "react-router-dom"
import { useAirports } from "../hooks/useAirports"
import { Select } from './select'


export const SearchBar = () => {

  const { airports } = useAirports()
  const navigate = useNavigate();

  const { data, error, isLoading } = airports

  const [ origin, setOrigin ] = useState<string | null>(null)
  const [ destination, setDestination ] = useState<string | null>(null)

  const origins = useMemo(
    () => data?.map(({airport_origin}) => ({ label: airport_origin.display_name, value: airport_origin.code }))
  , [data])

  const getDestinations = useCallback((origin: string | null) => {
    return data
      ?.find(ap => ap.airport_origin.code === origin)
      ?.airport_destinations?.map(dest => ({label: dest.display_name, value: dest.code})) ?? []

  }, [data])

  const handleOriginChange = (newValue: string) => {
    if (!getDestinations(newValue).some(d => d.value == newValue)) setDestination(null)
    setOrigin(newValue)
  }

  const getAirportCode = (airportName: string) => {

      const airports = data?.flatMap(x => [x.airport_origin, ...x.airport_destinations])

      return airports!.find(x => x.display_name === airportName)?.code ?? ''
  }


  const handleSubmit = () => {
    const params = new URLSearchParams()
    params.append('origin', origin)
    params.append('destination', destination)

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

    <Stack>
              <Autocomplete
          disablePortal
          isOptionEqualToValue={(option, value) => option === value}
          options={origins!}
          sx={{ minWidth: 300 }}
          onInputChange={handleOriginChange}
          value={origin}
          renderInput={(params) => 
            <TextField 
              {...params} 
              label="Origen" 
              className="bg-neutral-100"
            />
          }
        />
          <Autocomplete
            disablePortal
        options={getDestinations(origin)}
              isOptionEqualToValue={(option, value) => option === value}
              value={destination}
              onChange={(_, newValue) => setDestination(newValue)}
      sx={{ minWidth: 300 }}
      className="bg-neutral-100"
      renderInput={(params) => <TextField {...params} label="Destino" />}
      />



      <button
        disabled={!origin || !destination}
        className="bg-zinc-600 w-full md:w-fit dark:bg-orange-500 font-semibold text-neutral-100 rounded p-2 px-4 disabled:bg-zinc-400 disabled:text-zinc-200 dark:disabled:bg-orange-400 transition-all"
        onClick={handleSubmit}
      >
        Buscar
      </button>
    </Stack>
  )
}
