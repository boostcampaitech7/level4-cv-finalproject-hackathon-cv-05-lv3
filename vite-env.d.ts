/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_MAP_CLIENT_ID: string;
  }
  
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
  