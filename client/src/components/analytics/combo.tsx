import Chart from "react-google-charts"
import dayjs from "dayjs"

import { useFlightDetails } from "../../hooks/useFlightDetail"


export const Combo = ({ origin, destination }) => {

  const month = dayjs().month();
  const from_date = dayjs().month(month).startOf("month").format("YYYY-MM-DD");
  const to_date = dayjs().month(month).endOf("month").format("YYYY-MM-DD");

  const { data } = useFlightDetails({origin, destination, from_date, to_date})

  if (!data) return

  const comboData =[
    [
      "Dia",
      "Millas",
      "Precio maximo",
      "Precio promedio",
      "Precio minimo",
    ],
    ...data.details
    .filter(d => dayjs(d.flight_date).month() === dayjs().month())
    .map(d => [dayjs(d.flight_date).format("DD"), d.miles, data.miles_max, data.miles_mean, data.miles_min])
    .sort((a, b) => +a[0] - +b[0])
  ];

  const displayMonth = dayjs().locale("es").format("MMMM");

  const options = {
    title: `Variacion de precios en el mes de ${displayMonth}`,
    vAxis: { title: "Millas" },
    hAxis: { title: "Dia" },
    seriesType: "bars",
    series: { 
      1: { type: "line" },
      2: { type: "line" },
      3: { type: "line" },
    },
  };
  
  return (
    <section className="flex justify-center">
      <div className="p-5 overflow-x-auto h-full m-5 sm:w-[1050px] flex justify-center">
        <div className="h-full mt-5 p-5 sm:w-[925px] w-[650px]">
          <Chart
            chartType="ComboChart"
            width="100%"
            height="400px"
            data={comboData}
            options={options}
          />
        </div>
      </div>
    </section>
  )

}
