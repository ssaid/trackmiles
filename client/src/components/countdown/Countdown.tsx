import { FormEvent, FormEventHandler, useState } from 'react';
import { milleros_api } from '../../api/milleros_api';
import { useCountdown } from '../../hooks/useCountdown';
import { TimeBox } from './TimeBox';
import { useWindowSize } from '@uidotdev/usehooks';
import ReactConfetti from 'react-confetti';

export const Countdown = () => {

  const release = import.meta.env.VITE_RELEASE_DATE ?? '2023-07-01'
  const { days, hours, minutes, seconds } = useCountdown(new Date(release));
	const [isSent, setIsSent] = useState(false)
  const [error, setError] = useState<string | null >(null)

  const {width, height}  = useWindowSize()

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {

    e.preventDefault()

    //@ts-ignore
    const email = e.target.email.value

    milleros_api.post('/waitinglist/', { email })
      .then( _ => setIsSent(true) )
      .catch( e => setError(e.response?.data?.email[0] ?? "Ha ocurrido un error inesperado.") )

  }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex flex-col items-center justify-center text-neutral-300">
        <h1 className="md:text-8xl text-7xl font-bold italic">Milleros</h1>
        <h2 className="text-xl -mt-2 sm:text-xl md:text-2xl font-semibold mb-4">Adventure is out there</h2>
      </div>
      <div className="flex">
        <TimeBox label="Dias" content={days} />
        <TimeBox label="Horas" content={hours} />
        <TimeBox label="Minutos" content={minutes} />
        <TimeBox label="Segundos" content={seconds} />
      </div>
      {
        isSent 
          ? <p className='text-lg font-bold mt-4'>Prepara las valijas, pronto te contactaremos!</p>
          : 
          (
            <form 
              className='mt-8 flex flex-col gap-2 w-full items-center max-w-sm'
              onSubmit={handleSubmit}
            >
              <input 
                name='email' 
                type='email' 
                placeholder='Email' 
                className='p-2 rounded-md px-4 w-full bg-gray-100 hover:bg-gray-200 font-medium text-neutral-700' 
                required
              />
              <button 
                type='submit'
                className='p-2 rounded-md px-4 w-full text-neutral-100 bg-orange-500 hover:bg-orange-600 font-semibold cursor-pointer'
              >
                Quiero viajar!
              </button>
              {
                error && <p className='text-sm font-semibold flex-grow-0'>{error}</p>
              }
            </form>
        )
      }
      {
        isSent && <ReactConfetti width={width} height={height} />
      }
    </div>
  );
};
