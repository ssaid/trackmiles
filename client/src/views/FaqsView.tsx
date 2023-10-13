import { Accordion, AccordionDetails, AccordionSummary, Divider, Typography } from "@mui/material"
import { useFaqs } from "../hooks/useFaqs"
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import { Box, Container, Stack } from "@mui/system"
import { Link } from "react-router-dom"

import logo from '../assets/logo.png'


export const FaqsView = () => {

  const { faqs } = useFaqs()

  if (faqs) return (
    <Container maxWidth='xl'>
      <Stack p={2}  >
        <Link to='/'>
          <Stack flexDirection="row" gap={1} alignItems="center">
            <img src={logo} className="w-16 h-16"/>
            <Typography 
              variant="h3"
              className="italic"
              color="grey.300"
            >
              Milleros
            </Typography>
          </Stack>
        </Link>
      </Stack>

      <Stack px={2}  >
        <Typography 
          variant="h6"
        >
            Dudas frecuentes
        </Typography>
      </Stack>
      <Divider />

      <Container maxWidth='lg' sx={{ minHeight: '100vh', mt: 3, pb: 2 }}>
        {
          faqs.map(faq => (
            <Accordion key={faq.id}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
              >
                <Typography dangerouslySetInnerHTML={{__html: faq.question}} />
              </AccordionSummary>
              <AccordionDetails>
                <Typography dangerouslySetInnerHTML={{__html: faq.answer}} />
              </AccordionDetails>
            </Accordion>
          ))
        }
      </Container>
    </Container>
  )
  
}
