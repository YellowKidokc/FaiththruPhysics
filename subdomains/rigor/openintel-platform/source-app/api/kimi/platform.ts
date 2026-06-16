import type { Env } from "../lib/env";
import type { UserProfile } from "./types";

async function kimiRequest<T>(
  env: Env,
  path: string,
  token: string,
  init?: RequestInit,
): Promise<T | null> {
  const resp = await fetch(`${env.kimiOpenUrl}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      Authorization: `Bearer ${token}`,
      ...init?.headers,
    },
  });
  if (!resp.ok) {
    const text = await resp.text();
    console.warn(
      `[kimi] Request to ${path} failed (${resp.status}): ${text}`,
    );
    return null;
  }
  return resp.json() as Promise<T>;
}

export const users = {
  getProfile: (env: Env, token: string) =>
    kimiRequest<UserProfile>(env, "/v1/users/me/profile", token),
};
