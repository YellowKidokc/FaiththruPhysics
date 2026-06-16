import type { FetchCreateContextFnOptions } from "@trpc/server/adapters/fetch";
import type { User } from "@db/schema";
import { authenticateRequest } from "./kimi/auth";
import type { Env } from "./lib/env";

export type TrpcContext = {
  req: Request;
  resHeaders: Headers;
  env: Env;
  user?: User;
};

export function createContextFactory(env: Env) {
  return async function createContext(
    opts: FetchCreateContextFnOptions,
  ): Promise<TrpcContext> {
    const ctx: TrpcContext = { req: opts.req, resHeaders: opts.resHeaders, env };
    try {
      ctx.user = await authenticateRequest(env, opts.req.headers);
    } catch {
      // Authentication is optional here
    }
    return ctx;
  };
}
