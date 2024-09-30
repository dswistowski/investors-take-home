import path from "path"
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  preview: {
    port: 8081,
    strictPort: true,
  },
  server: {
    port: 8081,
    strictPort: true,
    host: true,
    origin: "http://0.0.0.0:8081",
  },
})
