/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        white: 'rgb(var(--color-bg) / <alpha-value>)',
        accent: 'rgb(var(--color-accent) / <alpha-value>)',
        gray: {
          50: 'rgb(var(--color-surface) / <alpha-value>)',
          100: 'rgb(var(--color-border) / <alpha-value>)',
          200: 'rgb(var(--color-border-strong) / <alpha-value>)',
          300: 'rgb(var(--color-border-strong) / <alpha-value>)',
          400: 'rgb(var(--color-text-muted) / <alpha-value>)',
          500: 'rgb(var(--color-text-muted) / <alpha-value>)',
          600: 'rgb(var(--color-text-muted) / <alpha-value>)',
          700: 'rgb(var(--color-text) / <alpha-value>)',
          800: 'rgb(var(--color-text) / <alpha-value>)',
          900: 'rgb(var(--color-text) / <alpha-value>)',
          950: 'rgb(var(--color-text-strong) / <alpha-value>)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        pixel: ['DotGothic16', 'monospace'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
