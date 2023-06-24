import { useToggleTheme } from "../hooks/useToggleTheme"
import { BsMoonStarsFill, BsFillSunFill } from 'react-icons/bs'

export const ToggleButton = () => {

  const { theme, themeToggler } = useToggleTheme()

  return (
    <div className='absolute right-5 top-5 transition duration-500 z-20'>
      <div 
        className="flex items-center justify-center w-full mb-12"
      >
        <label htmlFor="toggleTwo" className="flex items-center cursor-pointer select-none">
          <div className="relative">
          <input type="checkbox" id="toggleTwo" className="sr-only"
            onClick={() => themeToggler()}
          />
          <div className="block h-8 border-2 rounded-full w-14 border-stone-400"></div>
          <div className={`
            absolute 
            w-6 
            h-6 
            rounded-full 
            dot 
            ${theme == 'light' ? 'left-1' : 'right-1'} 
            top-1 
            transition
            duration-500
            flex
            justify-center
            items-center
            `}

          >
            { theme == 'dark' ? <BsMoonStarsFill color={'#78716c'} /> : <BsFillSunFill color="#fbbf24" /> }
          </div>
          </div>
        </label>

        </div>
        </div>
  )

}
