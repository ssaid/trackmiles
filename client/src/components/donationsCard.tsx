import { 
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  IconButton,
  Stack,
  Typography,
} from "@mui/material"
import { useState } from "react";

import CloseIcon from '@mui/icons-material/Close';
import cafecito from '../assets/cafecito_logo.svg';



export const DonationsCard = () => {
  const [open, setOpen] = useState(true);
  const [donated, setDonated] = useState(false);

  const handleClose = () => {
    setOpen(false);
  }

  const handleDonated = () => {
    setDonated(true);
    window.open('https://www.google.com.ar', '_blank')
  }


  return (
    <Box
      position="sticky"
      bottom={0}
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
                      <Button 
                        sx={{
                          py: 2
                        }}
                        variant='contained' 
                        onClick={handleDonated}
                      >
                        <Stack
                          direction='row'
                          gap={1}
                        >
                          <img src={cafecito}/>
                          <Typography fontWeight='bold' textAlign='center'>
                            Invitanos un Cafecito
                          </Typography>
                        </Stack>
                      </Button>
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
