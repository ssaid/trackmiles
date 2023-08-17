import { Backdrop, Box, Stack, Typography } from "@mui/material"
import { SearchBar } from "../components/SearchBar"

import bg from '../assets/bg.jpg'



export const HomeView = () => {
  
  return (
    <Stack
      height='100vh'
      position="relative"
    >
      <img 
        className="object-cover w-screen h-full absolute z-0"
        src={bg} 
      />
      <Backdrop open />
      <Box
        bgcolor='background.paper'
        position="absolute"
        bottom={0}
        height='35%'
        width='100%'
      >
        <Stack
          height='100%'
          justifyContent="end"
          alignItems="center"
          padding={10}

        >
          <Typography 
            variant="h2"
            className="italic"
            color="grey.300"
          >
            Milleros
          </Typography>
        </Stack>
      </Box>
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
          
        </Typography>

        <SearchBar />
      </Stack>
    </Stack>
  )
}
