import { eq } from "drizzle-orm";
import * as schema from "@db/schema";
import type { InsertUser } from "@db/schema";
import { getDb, type DbEnv } from "./connection";

export async function findUserByUnionId(env: DbEnv, unionId: string) {
  const rows = await getDb(env)
    .select()
    .from(schema.users)
    .where(eq(schema.users.unionId, unionId))
    .limit(1);
  return rows.at(0);
}

export async function upsertUser(env: DbEnv & { OWNER_UNION_ID?: string }, data: InsertUser) {
  const values = { ...data };
  const updateSet: Partial<InsertUser> = {
    lastSignInAt: new Date(),
    ...data,
  };

  if (
    values.role === undefined &&
    values.unionId &&
    values.unionId === env.OWNER_UNION_ID
  ) {
    values.role = "admin";
    updateSet.role = "admin";
  }

  await getDb(env)
    .insert(schema.users)
    .values(values)
    .onConflictDoUpdate({
      target: schema.users.unionId,
      set: updateSet,
    });
}
