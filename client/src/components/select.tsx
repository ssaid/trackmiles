import { useCallback, useEffect, useLayoutEffect, useRef, useState } from "react"
import { RxCross2 } from 'react-icons/rx'



type SelectProps = {
  options: Option[],
  onChange: (value: string) => void,
  className?: string,
  placeholder?: string,
  disabled?: boolean,
}

type Option = {
  value: string,
  label: string,
}

export const Select = ({options, onChange, ...props}: SelectProps) => {

  const [ filter, setFilter ] = useState<string>('')
  const [ isOpen, setIsOpen ] = useState<boolean>(false)

  const lastOptions = useRef<Option[]>([])

  useEffect(() => {

    if (JSON.stringify(lastOptions.current) !== JSON.stringify(options)) {
      if (!options.some(opt => opt.label === filter)){
        setFilter('')
        onChange(null)
      }
      lastOptions.current = options
    }

  }, [options])

  const handleSelect = ({ value, label }) => {
    setFilter(label)
    onChange(value)
    setIsOpen(false)
  }

  const filteredOptions = useCallback((filter: string): Option[] => {
    const match = options.some(opt => opt.label.toLowerCase() === filter.toLowerCase())

    return match ? options : options.filter(opt => opt.label.toLowerCase().includes(filter.toLowerCase()))

  }, [options])

  const handleFocus = () => {
    setIsOpen(true)
  }

  const handleBlur = () => {
    setTimeout(() => setIsOpen(false), 200)
  }

  const handleReset = () => {
    setFilter('')
    onChange(null)
  }

  return (

    <div className="relative w-full">
      <input 
        disabled={props.disabled}
        className="w-full dark:text-neutral-100 p-2 px-4 rounded bg-neutral-100 border border-neutral-500 focus:ring-0 focus:border-2 focus:border-indigo-300 focus:outline-none dark:bg-neutral-600 dark:placeholder:text-neutral-400 disabled:opacity-50" 
        onChange={(e) => setFilter(e.target.value)} 
        value={filter}
        onFocus={handleFocus}
        onBlur={handleBlur}
        placeholder={props.placeholder}
      />
      {
        !props.disabled && (
          <div
            className="absolute right-1 top-1 bg-neutral-100 dark:bg-neutral-600 p-1"
          >
            <div 
              onClick={handleReset}
              hidden={!filter}
              className="text-neutral-500 dark:text-neutral-400 dark:hover:bg-neutral-700  hover:bg-neutral-200 rounded-full cursor-pointer p-1 transition duration-300"
            >
              <RxCross2 />
            </div>
          </div>
        )

      }
      <div 
        className={ `bg-neutral-100 dark:bg-neutral-600 dark:border-neutral-500 dark:text-neutral-100 border border-neutral-200 rounded z-10 w-full absolute top-10 flex m-0 gap-0 flex-col p-1 ${isOpen && filteredOptions(filter).length ? 'block' : 'hidden'}`}
      >
        {
          filteredOptions(filter)
          .map(opt => 
            <option 
              className="cursor-pointer p-1 px-2 max-w-full h-full overflow-hidden"
              key={opt.value} 
              value={opt.value}
              onClick={() => handleSelect(opt)}
            >
              {opt.label}
            </option>
          )
        }
      </div>
    </div>

  )

}
