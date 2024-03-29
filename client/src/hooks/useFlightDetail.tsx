import { useQuery } from "@tanstack/react-query"
import { milleros_api } from "../api/milleros_api"
import { Flight } from "../interfaces"


type FlightDetailProps = {
  origin: string
  destination: string
  from_date?: string
  to_date?: string
}

const getFlightDetail = async (props: FlightDetailProps)  => {

  const params = new URLSearchParams()

  params.append('origin', props.origin)
  params.append('destination', props.destination)

  if (props.from_date) {
    params.append('from_date', props.from_date)
  }

  if (props.to_date) {
    params.append('to_date', props.to_date)
  }

  const { data } = await milleros_api.get<Flight>(`/flights/`, { params })

  return data
}



export const useFlightDetails = (props: FlightDetailProps) => {

  const flight = useQuery(
    ['flight', props],
    () => getFlightDetail(props),
  )

  return {
    flight,
    isLoading: flight.isLoading,
    error: flight.error,
    isError: flight.isError,
    data: flight.data,
  }

}
