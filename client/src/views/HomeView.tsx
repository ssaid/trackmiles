import { Stack } from "@mui/material"
import { SearchBar } from "../components/SearchBar"



export const HomeView = () => {
  
  return (
    <Stack 
      position="absolute"
      height='100%'
      width='100%'
      justifyContent="center"
      alignItems="center"

    >

      <SearchBar />
    </Stack>
  )
}
