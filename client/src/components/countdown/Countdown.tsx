import { FormEvent, useState } from 'react';
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

  const handleSubmit = (e) => {

    e.preventDefault()

    const email = e.target.email.value

    milleros_api.post('/waitinglist/', { email })
      .then( _ => setIsSent(true) )
      .catch( e => setError(e.response?.data?.email[0] ?? "Ha ocurrido un error inesperado.") )

  }

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-6xl font-bold mb-4">Milleros</h1>
      <h2 className="text-xl sm:text-2xl md:text-3xl font-bold mb-4">¿Ya pensaste en tu próximo destino?</h2>
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
                className='p-2 rounded-md px-4 w-full bg-gray-200 hover:bg-gray-300 font-medium text-neutral-600' 
                required
              />
              <button 
                type='submit'
                className='p-2 rounded-md px-4 w-full bg-red-600 hover:bg-red-500 font-medium cursor-pointer'
              >
                Avisame
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
