import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// base ./ supaya jalan di GitHub Pages (subpath) dan custom domain facebook.taufik.fyi
export default defineConfig({
  plugins: [react()],
  base: './',
})
