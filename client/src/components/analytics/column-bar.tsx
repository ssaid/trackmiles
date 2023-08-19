import Chart from "react-apexcharts";
import { Stack, Typography } from '@mui/material';

import dayjs from "dayjs"
import es from "dayjs/locale/es";

import { useFlightDetails } from "../../hooks/useFlightDetail"
import { ApexOptions } from "apexcharts";


export const ColumnBar = ({ origin, destination }) => {
  const month = dayjs().month(); 
  const from_date = dayjs().month(month).startOf("month").format("YYYY-MM-DD");
  const to_date = dayjs().month(month).endOf("month").format("YYYY-MM-DD");

  const { data } = useFlightDetails({origin, destination, from_date, to_date})

  if (!data) return

  const displayMonth = dayjs().locale(es).format("MMMM");

  const filteredSeries = data.details
      .filter(d => d.flight_date > from_date && d.flight_date < to_date)
      .sort((a, b) => dayjs(a.flight_date).diff(dayjs(b.flight_date)))
      .map(d => ({ x: dayjs(d.flight_date).format("DD"), y: d.miles }))


  const series: ApexOptions["series"] = [ 
    {
      name: 'Millas',
      data: filteredSeries
    }

  ]  

  const options: ApexOptions = {
    chart: {
      id: 'bar',
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      bar: {
        colors: {
          backgroundBarRadius: 0,
          ranges: [
            {
              from: 0,
              to: 10000000,
              color: '#1abc9c'
            }
          ],
        }
      }

    },
    tooltip: {
      enabled: false,
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      width: 0
    },
    xaxis: {
      title: {
        text: 'Día'
      }
    },
    yaxis: {
      title: {
        text: 'Millas'
      }
    }
  }

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
            <div className="min-w-[500px] w-full md: flex justify-center">
              <Chart 
                type='bar' 
                height='325px'
                series={series}
                options={options}
                style={{ width: '100%', maxWidth: '870px' }}
              />
            </div>
          </div>
        </Stack>
      </Stack>
    </>

  )

}
