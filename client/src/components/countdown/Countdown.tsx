import { FormEvent, useState } from 'react';
import { useCountdown } from '../../hooks/useCountdown';
import { TimeBox } from './TimeBox';

export const Countdown = () => {

  const { days, hours, minutes, seconds } = useCountdown(new Date('2023-07-01'));
	const [isSent, setIsSent] = useState(false)

	const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
		e.preventDefault()
		const email = e.target.email.value
		console.log(email)
		setIsSent(true)

	}

  return (
		<div className="flex flex-col items-center justify-center h-screen">
			<h1 className="text-6xl font-bold mb-4">Milleros</h1>
			<h2 className="text-2xl md:text-4xl font-bold mb-4">Cada vez falta menos!</h2>
			<div className="flex">
				<TimeBox label="Dias" content={days} />
				<TimeBox label="Horas" content={hours} />
				<TimeBox label="Minutos" content={minutes} />
				<TimeBox label="Segundos" content={seconds} />
			</div>
			{
				isSent 
					? <p className='text-2xl font-bold mt-4'>Gracias por suscribirte!</p>
					: 
					(
						<form 
							className='mt-8 flex flex-col gap-2'
							onSubmit={handleSubmit}
						>
							<input 
								name='email' 
								type='email' 
								placeholder='Email' 
								className='p-2 rounded-md px-4 bg-gray-200 hover:bg-gray-300 font-medium' 
								required
							/>
							<button 
								type='submit'
								className='p-2 rounded-md px-4 bg-red-600 hover:bg-red-500 font-medium cursor-pointer'
							>
								Se el primero en enterarte
							</button>
						</form>
				)
			}
		</div>
  );
};
