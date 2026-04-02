import type { Config } from 'tailwindcss'

export default {
  content: [
    './app.vue',
    './components/**/*.{vue,js,ts}',
    './pages/**/*.vue',
    './composables/**/*.{js,ts}',
    './stores/**/*.{js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f1faf7',
          100: '#dcf4ec',
          500: '#169873',
          600: '#137d5f',
          700: '#11674f',
        },
      },
      boxShadow: {
        soft: '0 10px 30px rgba(8, 43, 34, 0.08)',
      },
      fontFamily: {
        sans: ['"Manrope"', '"Segoe UI"', 'sans-serif'],
      },
    },
  },
  plugins: [],
} satisfies Config
