import bgImage from './assets/bg.jpg'
import { Countdown } from './components/countdown/Countdown'

function App() {

  return (

    <div className="w-auto h-screen relative">

		<div>
			<img 
				src={bgImage} 
				alt="background" 
				className="absolute object-cover w-full h-full -z-10"
			/>
		</div>
		<section className="bg-black bg-opacity-60 text-white-400 body-font text-white">
			<div className="container flex flex-col items-center justify-center h-screen px-5 py-24 mx-auto">
				<Countdown />
			</div>
		</section>


  </div>

  )
}

export default App
