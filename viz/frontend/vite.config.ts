import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    envDir: path.resolve(__dirname, "../.."),
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        port: 5173,
        proxy: {
            "/auth": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/token": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/api": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/typhoons": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/forecast": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/health": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/version": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/alerts": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
            "/subscriptions": {
                target: "http://127.0.0.1:8000",
                changeOrigin: true,
            },
        },
    },
    build: {
        // FastAPI serves this package directory; a successful build must update it.
        outDir: "../../src/typhoon_vn/dashboard",
        emptyOutDir: true,
        sourcemap: true,
        rollupOptions: {
            output: {
                manualChunks: {
                    "vendor-react": ["react", "react-dom"],
                    "vendor-map": ["leaflet"],
                },
            },
        },
    },
});
