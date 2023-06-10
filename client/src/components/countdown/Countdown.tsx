import { FormEvent, useState } from 'react';
import { milleros_api } from '../../api/milleros_api';
import { useCountdown } from '../../hooks/useCountdown';
import { TimeBox } from './TimeBox';

export const Countdown = () => {

  const release = import.meta.env.VITE_RELEASE_DATE ?? '2023-07-01'
  const { days, hours, minutes, seconds } = useCountdown(new Date(release));
	const [isSent, setIsSent] = useState(false)
  const [error, setError] = useState<string | null >(null)

	const handleSubmit = async(e: FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		const email = e.target.email.value
    try{
      const res = await milleros_api.post('/waitinglist/', { email })
      setIsSent(true)
    }catch(e){
      setError(e.response.data.email[0])

    }

	}

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-6xl font-bold mb-4">Milleros</h1>
      <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-4">¿Ya pensaste en tu próximo destino?</h2>
      <div className="flex">
        <TimeBox label="Dias" content={days} />
        <TimeBox label="Horas" content={hours} />
        <TimeBox label="Minutos" content={minutes} />
        <TimeBox label="Segundos" content={seconds} />
      </div>
      {
        isSent 
          ? <p className='text-lg font-bold mt-4'>Te estaremos contactando para que encuentres los mejores vuelos!</p>
          : 
          (
            <form 
              className='mt-8 flex flex-col gap-2 w-full items-center'
              onSubmit={handleSubmit}
            >
              <input 
                name='email' 
                type='email' 
                placeholder='Email' 
                className='p-2 rounded-md px-4 w-full bg-gray-200 hover:bg-gray-300 font-medium' 
                required
              />
              <button 
                type='submit'
                className='p-2 rounded-md px-4 w-full bg-red-600 hover:bg-red-500 font-medium cursor-pointer'
                >
                Se el primero en enterarte
              </button>
              {
                error && <p className='text-sm font-semibold flex-grow-0'>{error}</p>
              }
            </form>
        )
      }
    </div>
  );
};
