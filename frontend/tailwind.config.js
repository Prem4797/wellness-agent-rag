/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        apple: {
          bg: '#f5f5f7',       // Apple's classic light gray background
          text: '#1d1d1f',     // Apple's soft black text
          muted: '#86868b',
          user: '#007aff',     // iOS iMessage Blue
          ai: '#e9e9eb',       // iOS iMessage Light Gray
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'San Francisco', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}