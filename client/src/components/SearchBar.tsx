import { Autocomplete, Stack, TextField } from "@mui/material"
import { useCallback, useMemo, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAirports } from "../hooks/useAirports"


export const SearchBar = () => {

  const { airports } = useAirports()
  const navigate = useNavigate();

  const { data, error, isLoading } = airports

  const [ origin, setOrigin ] = useState<string | null>(null)
  const [ dest, setDest ] = useState<string | null>(null)

  const origins = useMemo(
    () => data?.map(({airport_origin}) => airport_origin.display_name)
  , [data])

  const getDestinations = useCallback((origin: string | null) => {
    return data
      ?.find(ap => ap.airport_origin.display_name === origin)
      ?.airport_destinations?.map(dest => dest.display_name) ?? []

  }, [data])

  const handleOriginChange = (_: any, newValue: string) => {
    if (!getDestinations(newValue).includes(dest)) setDest(null)
    setOrigin(newValue)
  }

  const getAirportCode = (airportName: string) => {

      const airports = data?.flatMap(x => [x.airport_origin, ...x.airport_destinations])

      return airports!.find(x => x.display_name === airportName)?.code ?? ''
  }


  const handleSubmit = () => {
    const params = new URLSearchParams()
    params.append('origin', getAirportCode(origin!))
    params.append('dest', getAirportCode(dest!))

    navigate(`/analytics?${params.toString()}`)

  }


  if (isLoading) return <p>Loading...</p>


  return (

    <div 
      className="flex flex-col lg:w-[90%] w-[95%] md:flex-row justify-center align-center gap-3 bg-neutral-100 p-8 rounded border-2 border-zinc-200"
    >
      <Autocomplete
        disablePortal
        options={origins!}
        sx={{ minWidth: 300 }}
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
        value={dest}
        onChange={(_, newValue) => setDest(newValue)}
        sx={{ minWidth: 300 }}
        renderInput={(params) => <TextField {...params} label="Destino" />}
      />


      <button
        disabled={!origin || !dest}
        className="bg-zinc-600 text-neutral-100 rounded p-2 px-4 disabled:bg-zinc-400 disabled:text-zinc-200 transition-all"
        onClick={handleSubmit}
      >
        Buscar
      </button>
    </div>
  )
}
