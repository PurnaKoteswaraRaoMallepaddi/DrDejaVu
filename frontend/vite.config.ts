import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on("proxyReq", (proxyReq, req) => {
            console.log(`[vite-proxy] ${req.method} ${req.url} -> http://localhost:8000${req.url}`);
          });
          proxy.on("proxyRes", (proxyRes, req) => {
            console.log(`[vite-proxy] ${req.method} ${req.url} <- ${proxyRes.statusCode}`);
          });
          proxy.on("error", (err, req) => {
            console.error(`[vite-proxy] ERROR ${req.method} ${req.url}:`, err.message);
          });
        },
      },
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
  },
});
