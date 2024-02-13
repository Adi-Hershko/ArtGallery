import { defineConfig } from 'vite';
import dotenv from 'dotenv';
import path from 'path';

// Manually load the .env file from the project root
const rootEnv = dotenv.config({ path: path.resolve(__dirname, '..', '.env') }).parsed;

// Convert the loaded environment variables for use with Vite
const envWithVitePrefix = Object.fromEntries(
  Object.entries(rootEnv || {}).map(([key, value]) => [`VITE_${key}`, `"${value}"`])
);

export default defineConfig({
  define: {
    'process.env': envWithVitePrefix,
  },
  // Your Vite configuration...
});
