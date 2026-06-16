import { drizzle } from "drizzle-orm/d1";
import * as schema from "@db/schema";
import * as relations from "@db/relations";

const fullSchema = { ...schema, ...relations };

export type DbEnv = {
  DB: D1Database;
};

export function getDb(env: DbEnv) {
  return drizzle(env.DB, { schema: fullSchema });
}
