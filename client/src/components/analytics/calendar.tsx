import { useMediaQuery } from "@mui/material";
import { Chart, ChartWrapperOptions, ReactGoogleChartEvent } from 'react-google-charts';
import ReactDOMServer from 'react-dom/server';

import { Flight, Detail } from "../../interfaces";
import { MdAirlineSeatReclineNormal, MdAirlineStops, MdOutlineAttachMoney } from "react-icons/md";
import { BsCalendarDate, BsClockHistory } from "react-icons/bs";
import { LuBaggageClaim } from "react-icons/lu";
import { ImPriceTags } from "react-icons/im";


type CalendarProps = {
  data: Flight
}

type TooltipProps = {
  detail: Detail
}

const Tooltip = ({ detail }: TooltipProps) => (
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

export const Calendar = ({ data }: CalendarProps) => {

  const isMobile = useMediaQuery('(max-width: 640px)')

  const chartEvents: ReactGoogleChartEvent[] = [
    {
      eventName: 'select',
      callback: (props) => {
        const chart = props.chartWrapper.getChart()
        const [selection] = chart.getSelection()
        if (!selection?.row) return
        console.log(`Origen: ${data.origin}`)
        console.log(`Destino: ${data.dest}`)
        console.log(`Fecha: ${data.details[selection.row].flight_date}`)
      }
    },
    {
      eventName: 'ready',
      callback : ( props ) => {
        
        const chart = props.chartWrapper.getChart()
        //@ts-ignore
        const textElements = chart.getContainer().getElementsByTagName('text')
        //@ts-ignore
        const barElements = chart.getContainer().getElementsByTagName('path')

        if (textElements.length > 1) {
          textElements[1].setAttribute('display', 'none')
          textElements[2].setAttribute('display', 'none')
        }

        if (barElements.length > 1) {
          barElements[2].setAttribute('display', 'none')
          barElements[3].setAttribute('display', 'none')
        }
      }
    }
  ];

  const calendarData = [
    [
      { type: "date", id: "Date" },
      { type: "number", id: "Price" },
      { type: "string", role: "tooltip", p: { isHtml: true } },
    ],
    ...data.details.map(
      detail => [
        new Date(detail.flight_date), 
        detail.porcentual, 
        ReactDOMServer.renderToString(<Tooltip detail={detail}/>),
      ]
    )
  ];


  const options: ChartWrapperOptions['options'] = {
    tooltip: { isHtml: true },
    colorAxis: {
      colors: ['#00b894', '#e74c3c'],
      // colors: ['#3498db', '#f39c12'],
      // colors: ['#9b59b6', '#f1c40f'],
      // colors: ['#1abc9c', '#e91e63'],
      // colors: ['#333333', '#aaaaaa']
    },
    legend: 'none',
    calendar: {
      legend: 'none',
      cellSize: isMobile ? 10 : 15,
      dayOfWeekLabel: {
        fontName: 'Poppins',
        fontSize: 12,
        bold: true,
      },
      dayOfWeekRightSpace: 10,
      daysOfWeek: 'DLMMJVS',
      monthLabel: {
        fontName: 'Poppins',
        fontSize: 16,
        bold: true,
      },
      underMonthSpace: 10,
      yearLabel: {
        fontName: 'Poppins',

      },
    },
    fontName: 'Poppins',

  }

  return (

      <section className="flex justify-center">
        <div className="p-5 overflow-x-auto h-full m-5 sm:w-[1050px] flex justify-center">
          <div className="h-full mt-5 p-5 sm:w-[925px] w-[650px]">
            <Chart
              chartType="Calendar"
              width="100%"
              height={ isMobile ? "250px" : "325px" }
              data={calendarData}
              options={options}
              chartEvents={chartEvents}
            />

          </div>
        </div>
      </section>
    

  )
}
