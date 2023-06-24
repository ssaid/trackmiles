import { MdAirplanemodeInactive } from 'react-icons/md'
import { Navigate } from 'react-router-dom'


export const ErrorView = () => {

  const handleReload = () => {
    if (window.location.pathname === '/')
      window.location.reload()

    return <Navigate to="/" />
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Error!</h1>
      <p className="text-lg flex items-center gap-2">Lo sentimos, pero ha ocurrido un error <MdAirplanemodeInactive /></p>
      <button 
        className="mt-4 px-4 py-2 bg-white text-neutral-700 font-semibold rounded-sm shadow"
        onClick={handleReload}
      >
        Volver
      </button>
    </div>
  )

}
