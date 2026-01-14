import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/video_feed': 'http://localhost:5000',
      '/get_text': 'http://localhost:5000',
      '/reset': 'http://localhost:5000',
      '/correct': 'http://localhost:5000',
      '/add_space': 'http://localhost:5000',
      '/delete_letter': 'http://localhost:5000',
    }
  }
})
