
export interface Flight {
  origin: string
  dest: string
  details: Detail[]
}

export interface Detail {
  flight_date: string
  provider: string
  external_link: string
  money: number
  miles: number
  seats: number | null
  duration: number | null
  stops: number | null
  baggage: boolean
  created_at: string
}
