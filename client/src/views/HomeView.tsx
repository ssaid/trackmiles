import { Backdrop, Box, Stack, Typography } from "@mui/material"
import { SearchBar } from "../components/SearchBar"

import bg from '../assets/bg.jpg'



export const HomeView = () => {
  
  return (
    <>
      <img 
        className="object-cover w-screen absolute z-0 h-full"
        src={bg} 
      />
      <Backdrop open />
      <Box
        bgcolor='background.paper'
        position="absolute"
        bottom={0}
        height='35%'
        width='100%'
      ></Box>
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
          color="grey.300"
        >
          Milleros
        </Typography>

        <SearchBar />
      </Stack>
    </>
  )
}
