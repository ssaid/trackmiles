import { useQuery } from "@tanstack/react-query"
import { milleros_api } from "../api/milleros_api"
import { OriginDestinations } from "../interfaces/airports"



const getAirports = async () => {
  const { data } = await milleros_api.get<OriginDestinations[]>('/airports/')

  return data
}



export const useAirports = () => {

  const airports = useQuery(
    ['airports'],
    getAirports,
    {
      staleTime: 1000 * 60 * 60 * 6, // 6 hours
      cacheTime: 1000 * 60 * 60 * 6, // 6 hours
    }
  )



  return {
    airports,
  }

}
