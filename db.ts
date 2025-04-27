import { Pool } from "pg";

export const pool = new Pool({
  user: "admin",
  password: "root",
  database: "bibliotech",
  port: 5432,
  host: "localhost",
});
