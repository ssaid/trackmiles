
export interface Flight {
  origin: string
  dest: string
  miles_median: number
  miles_max: number
  miles_min: number
  miles_mean: number
  details: Detail[]
}

export interface Detail {
  flight_date: string
  provider: string
  porcentual: number
  external_link: string
  money: number
  miles: number
  seats: number | null
  duration: number | null
  stops: number | null
  baggage: boolean
  created_at: string
}
