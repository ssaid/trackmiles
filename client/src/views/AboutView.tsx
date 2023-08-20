import { Accordion, AccordionDetails, AccordionSummary, Divider, Typography } from "@mui/material"
import { useFaqs } from "../hooks/useFaqs"
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import { Box, Container, Stack } from "@mui/system"
import { Link } from "react-router-dom"



export const AboutView = () => {

  const { faqs } = useFaqs()

  if (faqs) return (
    <Container maxWidth='xl'>
      <Stack p={2}  >
        <Typography 
          variant="h3"
          className="italic"
        >
          <Link to='/'>
            Milleros
          </Link>
        </Typography>
      </Stack>

      <Stack px={2}  >
        <Typography 
          variant="h6"
        >
            Dudas frecuentes
        </Typography>
      </Stack>
      <Divider />

      <Container maxWidth='lg' sx={{ minHeight: '100vh', mt: 3 }}>
        {
          faqs.map(faq => (
            <Accordion key={faq.id}>
              <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1a-content"
                id="panel1a-header"
              >
                  <div dangerouslySetInnerHTML={{__html: faq.question}}/>
              </AccordionSummary>
              <AccordionDetails>
                  <div dangerouslySetInnerHTML={{__html: faq.answer}}/>
              </AccordionDetails>
            </Accordion>
          ))
        }
      </Container>
    </Container>
  )
  
}
