import { createClient } from "@libsql/client";
import { configDotenv } from "dotenv";

export const db = createClient({
  url: process.env.TURSO_DB_URL,
  authToken: process.env.TURSO_DB_TOKEN,
});

configDotenv();