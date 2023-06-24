import { useQuery } from "react-query"
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
  )



  return {
    airports,
  }

}
