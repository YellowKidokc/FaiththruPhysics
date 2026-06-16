/// <reference types="@cloudflare/workers-types" />

export type WorkerEnv = {
  APP_ID: string;
  APP_SECRET: string;
  KIMI_AUTH_URL: string;
  KIMI_OPEN_URL: string;
  OWNER_UNION_ID?: string;
  DB: D1Database;
};

function required(env: WorkerEnv, name: keyof WorkerEnv): string {
  const value = env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value as string;
}

export function createEnv(env: WorkerEnv) {
  return {
    APP_ID: env.APP_ID,
    APP_SECRET: env.APP_SECRET,
    KIMI_AUTH_URL: env.KIMI_AUTH_URL,
    KIMI_OPEN_URL: env.KIMI_OPEN_URL,
    OWNER_UNION_ID: env.OWNER_UNION_ID,
    DB: env.DB,
    appId: required(env, "APP_ID"),
    appSecret: required(env, "APP_SECRET"),
    kimiAuthUrl: required(env, "KIMI_AUTH_URL"),
    kimiOpenUrl: required(env, "KIMI_OPEN_URL"),
    ownerUnionId: env.OWNER_UNION_ID ?? "",
  };
}

export type Env = ReturnType<typeof createEnv>;
