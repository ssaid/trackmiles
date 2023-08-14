import {
  Chart as ChartJS,
  LinearScale,
  CategoryScale,
  BarElement,
  PointElement,
  LineElement,
  Legend,
  Tooltip,
  LineController,
  BarController,
  ChartData,
} from 'chart.js';
import { Chart, ChartProps } from 'react-chartjs-2';

import dayjs from "dayjs"
import es from "dayjs/locale/es";

import { useFlightDetails } from "../../hooks/useFlightDetail"
import { Stack, Typography } from '@mui/material';


export const Combo = ({ origin, destination }) => {
const month = dayjs().month(); const from_date = dayjs().month(month).startOf("month").format("YYYY-MM-DD");
  const to_date = dayjs().month(month).endOf("month").format("YYYY-MM-DD");

  const { data } = useFlightDetails({origin, destination, from_date, to_date})

  if (!data) return


  ChartJS.register(
    LinearScale,
    CategoryScale,
    BarElement,
    PointElement,
    LineElement,
    Legend,
    Tooltip,
    LineController,
    BarController
  );

  const displayMonth = dayjs().locale(es).format("MMMM");

  const dataSet: ChartData = {
    labels: data.details.map(d => dayjs(d.flight_date)
              .format("DD"))
              //@ts-ignore
              .sort((a, b) => a - b),
    datasets: [
      {
        type: 'bar' as const,
        label: 'Millas',
        backgroundColor: '#00b894',
        data: data.details.map(d => d.miles),
        borderColor: 'gray',
        borderWidth: 2,
      },
    ],
     
  };

  const options = {
    font: {
      size: 18,
      family: 'Poppins'

    },
    plugins: {
      legend: {
        display: false 
      },
      tooltip: {
      callbacks: {
        title: () => '',
        label: (ctx) => `Millas: ${ctx.parsed.y}`
      }
    }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Día',
          font: {
            size: 14,
          }
        },
      },
      y: {
        title: {
          display: true,
          text: 'Millas',
          font: {
            size: 14,
          }
        },
      }
    },
    grid: {
      display: false
    }
  };

  
  return (
    <>
      <Typography
        variant='h6'
        align='center'
        fontWeight='bold'
        mt={2}
      >
        Millas en el mes de { displayMonth } 🔥
      </Typography>

      <Stack justifyContent='center'>
        <Stack
          p={2}
          maxWidth='screen'
          mt={2}
        >
          <div className="p-1 overflow-x-auto h-full max-w-screen">
              <div className="max-h-[450px] min-w-[700px] w-full flex justify-center">
                <Chart 
                  type='bar' 
                  data={dataSet}  
                  options={options}
                />
              </div>
          </div>
        </Stack>
      </Stack>
    </>

  )

}




