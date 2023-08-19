import ReactDOMServer from 'react-dom/server';
import { Stack, Typography, useMediaQuery } from "@mui/material";
import { ApexOptions } from "apexcharts";
import Chart from "react-apexcharts";
import dayjs from "dayjs"; import es from "dayjs/locale/es";

import { Detail, Flight } from "../../interfaces";
import { memo, useCallback } from "react";


import { MdAirlineSeatReclineNormal, MdAirlineStops, MdOutlineAttachMoney } from "react-icons/md";
import { BsCalendarDate, BsClockHistory } from "react-icons/bs";
import { LuBaggageClaim } from "react-icons/lu";
import { ImPriceTags } from "react-icons/im";

type TooltipProps = {
  detail: Detail
}


const Tooltip = ({ detail }: TooltipProps) => {

  if (detail) return (
    <div className="flex flex-col text-neutral-800 w-40 text-sm p-2">
      { detail.flight_date ? <span className="flex items-center gap-1"><BsCalendarDate /> Fecha: { detail.flight_date }</span> : ''}
      { detail.miles ? <span className="flex items-center gap-1"><ImPriceTags /> Millas: { detail.miles.toLocaleString('es') }</span> : ''}
      { detail.money ? <span className="flex items-center gap-1"><MdOutlineAttachMoney /> Precio: { detail.money.toLocaleString('es') }</span> : ''}
      { detail.stops ? <span className="flex items-center gap-1"><MdAirlineStops /> Escalas: { detail.stops }</span> : ''}
      { detail.duration ? <span className="flex items-center gap-1"><BsClockHistory /> Duracion: { detail.duration }h</span> : ''}
      { detail.seats ? <span className="flex items-center gap-1"><MdAirlineSeatReclineNormal /> Asientos: { detail.seats }</span> : ''}
      { <span className="flex items-center gap-1"><LuBaggageClaim /> Equipaje: { detail.baggage ? 'Si' : 'No'}</span> }
    </div>
  )

}
type HeatMapProps = {
  data: Flight
}

export const HeatMap = memo(({ data }: HeatMapProps) => {

  const parseData = useCallback( (data: Flight) => {
    const result: { [name: string]: {x: string, y: number}[] }  = {}
    for ( let detail of data.details){
      const name = dayjs(detail.flight_date).locale(es).format("MMMM YYYY")
      if (! result.hasOwnProperty(name)) result[name] = []

      result[name].push({
        x: dayjs(detail.flight_date).format("DD"),
        y: detail.porcentual,
      })
    }
    return result

  }, [data])
  
  const series: ApexOptions["series"] = Object.entries(parseData(data))
    .map( ([name, data]) => ({
      name,
      data: data.sort( (a, b) => parseInt(a.x) - parseInt(b.x))
    }))



  const options: ApexOptions = {
    chart: {
      id: 'heatmap',
      toolbar: {
        show: false
      }
    },
    plotOptions: {
      heatmap: {
        shadeIntensity: 0.5,
        colorScale: {
          ranges: [{
            from: -100,
            to: -26,
            name: 'Muy Baratos',
            color: '#00A100'
          },
            {
              from: -25,
              to: -11,
              name: 'Baratos',
              color: '#128FD9'
            },
            {
              from: -10,
              to: 10,
              name: 'Promedio',
              color: '#fff133' //yellow
            },
            {
              from: 11,
              to: 25,
              name: 'Caros',
              color: '#FFB200' //orange
            },
            {
              from: 26,
              to: 100,
              name: 'Muy Caros',
              color: '#FF0000'
            }
          ]
        }
      },
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      width: 1
    },
    tooltip: {
      custom: ({ seriesIndex, dataPointIndex, w }) => {

        const [ month, year ] = w.globals.seriesNames[seriesIndex].split(' ')
        const date = `${w.globals.labels[dataPointIndex]} ${month} ${year}`
        const formatedDate = dayjs(date, 'DD MMMM YYYY', 'es').format('YYYY-MM-DD')

        const detail = data.details.find( d => dayjs(d.flight_date).locale(es).format('DD MMMM YYYY') === date )

        return ReactDOMServer.renderToString(<Tooltip detail={detail}/>)

      }
    },
    xaxis: {
      type: 'category',
      categories: Array.from({length: 31}, (_, i) => `${ i + 1 }`.padStart(2, '0')),
    },

  }



  return (
    <>
      <Typography
        variant='h6'
        align='center'
        fontWeight='bold'
        mt={2}
      >
        Mapa anual 🗓️
      </Typography>
      <Stack justifyContent='center'>
        <Stack
          p={2}
          maxWidth='screen'
        >
          <div className="p-1 overflow-x-auto h-full max-w-screen">
            <div className="mx-auto sm:w-[925px] w-[650px]">
              <Chart
                height={350}
                options={options}
                type="heatmap"
                series={series}
              />

            </div>
          </div>
        </Stack>
      </Stack>
    </>
  )
})
