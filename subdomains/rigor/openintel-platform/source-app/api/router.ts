import { authRouter } from "./auth-router";
import { openintelRouter } from "./openintel-router";
import { scoringRouter } from "./scoring-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  openintel: openintelRouter,
  scoring: scoringRouter,
});

export type AppRouter = typeof appRouter;
