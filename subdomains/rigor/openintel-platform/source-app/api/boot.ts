import { Hono } from "hono";
import { bodyLimit } from "hono/body-limit";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "./router";
import { createContextFactory } from "./context";
import { createEnv, type WorkerEnv } from "./lib/env";
import { createOAuthCallbackHandler } from "./kimi/auth";
import { Paths } from "@contracts/constants";

const app = new Hono<{ Bindings: WorkerEnv }>();

app.use(bodyLimit({ maxSize: 50 * 1024 * 1024 }));

app.get(Paths.oauthCallback, (c) => {
  const env = createEnv(c.env);
  return createOAuthCallbackHandler(env)(c);
});

app.use("/api/trpc/*", async (c) => {
  const env = createEnv(c.env);
  const createContext = createContextFactory(env);
  return fetchRequestHandler({
    endpoint: "/api/trpc",
    req: c.req.raw,
    router: appRouter,
    createContext,
  });
});

app.all("/api/*", (c) => c.json({ error: "Not Found" }, 404));

export default app;
