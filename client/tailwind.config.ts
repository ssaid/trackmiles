/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend:
    {
      fontFamily: {
        'poppins': ['Poppins', 'sans-serif']
      },

      colors: ({theme}) => ({
        'button-bg-dark': theme('bg-orange-500'),

      })
      
    },
  },
  plugins: [],
}

