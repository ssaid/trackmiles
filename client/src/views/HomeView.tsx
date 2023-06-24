import { Stack } from "@mui/material"
import { SearchBar } from "../components/SearchBar"
import { Wave } from "../components/Wave"
import bgImage from '../assets/bg.jpg'



export const HomeView = () => {
  
  return (
    <div>
      <div className="absolute inset-0">
        <img 
          src={bgImage} 
          alt="background" 
          className="absolute object-cover w-full h-full -z-10"
        />
        <div className="absolute inset-0 bg-black opacity-60"></div>
      </div>

      <div className="absolute h-screen w-screen flex flex-col justify-end object-fill">
        <Wave/>
        <div className='h-[35%] w-screen bg-neutral-100 dark:bg-neutral-800 transition-all'>
          <div className="flex flex-col justify-end p-10 items-center h-full">
            Milleros
          </div>
        </div>
      </div>
      <Stack 
        position="absolute"
        height='100%'
        width='100%'
        justifyContent="center"
        alignItems="center"

      >

        <SearchBar />
      </Stack>
    </div>
  )
}
