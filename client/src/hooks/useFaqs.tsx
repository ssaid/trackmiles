import { useQuery } from "@tanstack/react-query"
import { milleros_api } from "../api/milleros_api"
import { Faq } from "../interfaces/faqs"



const getFaqs = async () => {
  const { data } = await milleros_api.get<Faq[]>('/faqs/')

  return data
}



export const useFaqs = () => {

  const query = useQuery(
    ['faqs'],
    getFaqs,
    {
      staleTime: 1000 * 60 * 60 * 6, // 6 hours
      cacheTime: 1000 * 60 * 60 * 6, // 6 hours
    }
  )



  return {
    faqs: query.data,
    query

  }

}
