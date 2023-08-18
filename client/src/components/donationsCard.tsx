import { 
  Box,
  Card,
  CardActions,
  CardContent,
  IconButton,
  Stack,
  Typography,
} from "@mui/material"
import { useState } from "react";

import CloseIcon from '@mui/icons-material/Close';



export const DonationsCard = () => {
  const [open, setOpen] = useState(true);
  const [donated, setDonated] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleDonated = () => {
    setDonated(true);
    window.open('https://cafecito.app/milleros', '_blank')
  }


  return (
    <Box
      position="sticky"
      bottom={0}
      zIndex={1000}
    >
      <Box
        position="absolute"
        bottom={0}
        right={0}
        m={1}
        display={open ? 'block' : 'none'}
      >
        <Card 
          elevation={3}
          sx={{ 
          maxWidth: {xs: '100%',  sm: 400 },
          height: 200,
          display: 'flex', 
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <CardActions>
            <IconButton 
              onClick={() => handleClose()}
              sx={{
                position: 'absolute',
                top: 8,
                right: 8,
              }}
            >
              <CloseIcon />
            </IconButton>
          </CardActions>
          <CardContent>
            <Stack
              mt={2}
              p={1}
              direction='column'
              alignItems='center'
              justifyContent='center'
              spacing={2}
            >
              {
                !donated 
                  ? 
                  (
                    <>
                      <Typography fontWeight='bold' textAlign='center'>
                        ¡Ayudanos a seguir creciendo y sé parte del crecimiento de Milleros!
                      </Typography>
                      <img 
                        style={{ cursor: 'pointer' }}
                        src='https://cdn.cafecito.app/imgs/buttons/button_1.svg'
                        onClick={handleDonated}
                      />
                    </>

                  ) 
                  : 
                  (
                    <Stack alignItems='center' height='100%'>
                      <Typography fontWeight='bold' textAlign='center'>
                        ¡Gracias por ayudarnos, esto nos motiva a seguir desarrollando la app! 💖
                      </Typography>
                    </Stack>
                  )
              }
            </Stack>
          </CardContent>
        </Card>
      </Box>
    </Box>

  )
}
