/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./ui/src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        singularity: {
          950: '#020617',
          900: '#0f172a',
          800: '#1e293b',
        }
      }
    },
  },
  plugins: [],
}
