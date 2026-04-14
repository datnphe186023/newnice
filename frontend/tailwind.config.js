/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
    './error.vue',
  ],
  theme: {
    extend: {
      colors: {
        // Primary: deep charcoal/black — matches logo background
        primary: {
          50:  '#f5f5f5',
          100: '#e8e8e8',
          200: '#d1d1d1',
          300: '#a8a8a8',
          400: '#737373',
          500: '#404040',
          600: '#262626',
          700: '#1a1a1a',
          800: '#111111',
          900: '#0a0a0a',
          950: '#050505',
        },
        // Accent: vivid red — automotive energy
        accent: {
          DEFAULT: '#e11d48',
          50:  '#fff1f2',
          100: '#ffe4e6',
          500: '#e11d48',
          600: '#be123c',
          700: '#9f1239',
        },
        dark: {
          DEFAULT: '#111111',
          100: '#1a1a1a',
          200: '#262626',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      container: {
        center: true,
        padding: {
          DEFAULT: '1rem',
          sm: '2rem',
          lg: '4rem',
          xl: '5rem',
        },
      },
    },
  },
  plugins: [],
}
