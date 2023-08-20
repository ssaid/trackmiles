import ReactDOMServer from 'react-dom/server';
import { Stack, Typography, useMediaQuery } from "@mui/material";
import { ApexOptions } from "apexcharts";
import Chart from "react-apexcharts";
import dayjs from "dayjs"; import es from "dayjs/locale/es";

import { Detail, Flight } from "../../interfaces";
import { memo, useCallback, useMemo } from "react";


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

  const isMobile = useMediaQuery('(max-width: 600px)')

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
      data: Array.from({length: 31}, (_, i) => data.find( d => d.x === `${ i + 1 }`.padStart(2, '0'))?.y ?? 1000000)
    }))


  const maxPorcentual = useMemo(() => Math.max(...data.details.map( d => d.porcentual)),[data])
  const minPorcentual = useMemo(() => Math.min(...data.details.map( d => d.porcentual)),[data])

  const cheap = (0 + minPorcentual) / 3
  const cheapest = cheap * 2
  const expensive = (0 + maxPorcentual) / 3
  const mostExpensive = expensive * 2

  /*
   *
   * [minPorcentual, cheapest) => Muy Baratos
   * [cheapest, cheap) => Baratos
   * [cheap, expensive) => Promedio
   * [expensive, mostExpensive) => Caros
   * [mostExpensive, maxPorcentual] => Muy Caros
   *
   */

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
          ranges: [
            {
            from: minPorcentual,
            to: cheapest,
            name: 'Muy Baratos',
            color: '#22c55e'
            },
            {
              from: cheapest + 0.001,
              to: cheap,
              name: 'Baratos',
              color: '#1d4ed8'
            },
            {
              from: cheap + 0.001,
              to: expensive,
              name: 'Promedio',
              color: '#eab308'
            },
            {
              from: expensive + 0.001,
              to: mostExpensive,
              name: 'Caros',
              color: '#f97316'
            },
            {
              from: mostExpensive + 0.001,
              to: maxPorcentual,
              name: 'Muy Caros',
              color: '#dc2626'
            },
            {
              from: 999999,
              to: 1000002,
              color: '#525252' ,
              name: 'Sin Datos'
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
          <div className="p-1 overflow-x-auto h-full max-w-screen overflow-y-clip">
            <div className="mx-auto sm:w-[925px] w-[625px]">
              <Chart
                height={ isMobile ? 250 : 350}
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
