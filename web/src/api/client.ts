import type { RunListItem, RunStatus } from "./types";

/*
 * The daemon read client. Same-origin in dev (Vite proxies /runs -> the daemon
 * sidecar), so paths are relative. A non-2xx or network failure throws; screens
 * catch it and render the one recovery action (states doctrine).
 */

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`GET ${url} failed (${res.status})`);
  }
  return (await res.json()) as T;
}

/** GET /runs — every run, newest first (error items included, never dropped). */
export function fetchRuns(): Promise<RunListItem[]> {
  return getJson<RunListItem[]>("/runs");
}

/** GET /runs/{id}/status — one run's projected status. */
export function fetchStatus(id: string): Promise<RunStatus> {
  return getJson<RunStatus>(`/runs/${encodeURIComponent(id)}/status`);
}
