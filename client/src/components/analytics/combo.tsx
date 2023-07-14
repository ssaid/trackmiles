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
import { Chart } from 'react-chartjs-2';

import dayjs from "dayjs"
import es from "dayjs/locale/es";

import { useFlightDetails } from "../../hooks/useFlightDetail"


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
        type: 'line' as const,
        label: 'Maximo',
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgb(255, 99, 132)',
        borderWidth: 2,
        fill: false,
        data: data.details.map(d => data.miles_max),
      },
      {
        type: 'line' as const,
        label: 'Promedio',
        borderColor: 'rgb(255, 255, 132)',
        backgroundColor: 'rgb(255, 255, 132)',
        borderWidth: 2,
        fill: false,
        data: data.details.map(d => data.miles_mean),
      },
      {
        type: 'line' as const,
        label: 'Minimo',
        borderColor: 'rgb(132, 255, 132)',
        backgroundColor: 'rgb(132, 255, 132)',
        borderWidth: 2,
        fill: false,
        
        data: data.details.map(d => data.miles_min),
      },
      {
        type: 'bar' as const,
        label: 'Millas',
        backgroundColor: 'rgb(75, 192, 192)',
        data: data.details.map(d => d.miles),
        borderColor: 'white',
        borderWidth: 2,
      },
    ],
  };

  
  return (
    <section className="flex justify-center flex-col items-center">
      <h4>Millas en el mes de { displayMonth }</h4>
      <div className="p-5 overflow-x-auto h-full m-5 sm:w-[1050px] flex justify-center">
          <Chart type='bar' data={dataSet}  />
      </div>
    </section>
  )

}




