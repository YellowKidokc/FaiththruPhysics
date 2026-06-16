import { drizzle } from "drizzle-orm/d1";
import { Hono } from "hono";
import { seedDatabase } from "../db/seed";
import * as schema from "../db/schema";
import type { WorkerEnv } from "./lib/env";

const app = new Hono<{ Bindings: WorkerEnv }>();

app.post("/", async (c) => {
  const db = drizzle(c.env.DB, { schema });
  await seedDatabase(db);
  return c.json({ success: true, message: "Database seeded" });
});

export default app;
