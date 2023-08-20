
export interface OriginDestinations {
  airport_origin: Airport
  airport_destinations: Airport[]
}

export interface Airport {
  display_name_long: string
  code: string
}

