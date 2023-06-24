import { Stack } from "@mui/material"
import { SearchBar } from "../components/SearchBar"
import { Wave } from "../components/Wave"



export const Home = () => {
  
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
