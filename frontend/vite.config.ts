import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // 사용 가능한 다른 포트로 변경
  },
  resolve: {
    alias: {
      "react-calendar": "/node_modules/react-calendar",
    },
  },
});
