/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#030712',
          900: '#060B18',
          850: '#0A1224',
          800: '#0E1A33',
          750: '#142344',
          700: '#1B2E56',
        },
        cyber: {
          cyan: '#00F0FF',
          blue: '#2563EB',
          sky: '#38BDF8',
          emerald: '#10B981',
          crimson: '#EF4444',
          amber: '#F59E0B',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2.5s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        scan: {
          '0%, 100%': { transform: 'translateY(0%)', opacity: '0.9' },
          '50%': { transform: 'translateY(100%)', opacity: '0.4' },
        },
        glow: {
          '0%': { boxShadow: '0 0 15px rgba(0, 240, 255, 0.25)' },
          '100%': { boxShadow: '0 0 30px rgba(0, 240, 255, 0.6)' },
        }
      },
      boxShadow: {
        'cyber-cyan': '0 0 25px -5px rgba(0, 240, 255, 0.3)',
        'cyber-blue': '0 0 25px -5px rgba(37, 99, 235, 0.35)',
        'cyber-crimson': '0 0 25px -5px rgba(239, 68, 68, 0.35)',
        'cyber-emerald': '0 0 25px -5px rgba(16, 185, 129, 0.35)',
      }
    },
  },
  plugins: [],
}
