import { Box, IconButton } from "@mui/material"
import { AiOutlineQuestionCircle } from "react-icons/ai"
import { Link } from "react-router-dom"


export const FaqButton = () => {

  return (
    <Box
      sx={{
        position: 'absolute',
        top: 40,
        right: 0,
        zIndex: 10,
        borderRadius: 1,
        p: 1,
      }}
    >
      <Link
        to='/about'
      >
        <IconButton 
          sx={{
            color: 'grey.400',
          }}
        >
          <AiOutlineQuestionCircle />
        </IconButton>
      </Link>
    </Box>
  )

}
