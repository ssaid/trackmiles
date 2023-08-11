import { Stack, Typography } from "@mui/material"
import { SearchBar } from "../components/SearchBar"



export const HomeView = () => {
  
  return (
    <Stack 
      position="absolute"
      height='100%'
      width='100%'
      justifyContent="space-evenly"
      alignItems="center"
    >
      <Typography 
        variant="h2"
        className="italic"
      >
        Milleros
      </Typography>

      <SearchBar />
    </Stack>
  )
}
