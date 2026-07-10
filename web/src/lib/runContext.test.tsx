import { renderHook, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import type { ReactNode } from "react";
import { act } from "react";
import { describe, expect, it } from "vitest";

import { RunProvider, useRun } from "./runContext";
import { server } from "../test/handlers";
import { statusReviewFrame, statusWorking } from "../test/fixtures";
import { jobLifecycle, succeededJob } from "../test/jobHandlers";

const RUN = "2026-07-04-spark-forest";

function wrapper({ children }: { children: ReactNode }) {
  return (
    <RunProvider runId={RUN} pollIntervalMs={5}>
      {children}
    </RunProvider>
  );
}

describe("runContext", () => {
  it("useRun throws outside a RunProvider (fail loud, not undefined)", () => {
    expect(() => renderHook(() => useRun())).toThrow(/RunProvider/);
  });

  it("provides the run's status read", async () => {
    const { result } = renderHook(() => useRun(), { wrapper });
    await waitFor(() => expect(result.current.status.status).toBe("ready"));
    expect(result.current.runId).toBe(RUN);
    if (result.current.status.status === "ready") {
      expect(result.current.status.data.run_id).toBe(RUN);
    }
    // idle run -> no job being watched
    expect(result.current.activeJob.status).toBe("idle");
  });

  it("refresh() re-reads the status", async () => {
    let reads = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        reads += 1;
        return HttpResponse.json(statusReviewFrame);
      }),
    );
    const { result } = renderHook(() => useRun(), { wrapper });
    await waitFor(() => expect(result.current.status.status).toBe("ready"));
    expect(reads).toBe(1);
    act(() => result.current.refresh());
    await waitFor(() => expect(reads).toBe(2));
  });

  it("polls the owning job while active_job is present, and re-reads the status once it goes terminal", async () => {
    // /status: working (job-7f3a owns the run) until the job wraps, then idle.
    // Assert via handler hit-counts (the 5ms lifecycle outruns waitFor samples).
    let statusReads = 0;
    let jobPolls = 0;
    server.use(
      http.get(`/runs/:id/status`, () => {
        statusReads += 1;
        return HttpResponse.json(statusReads === 1 ? statusWorking : statusReviewFrame);
      }),
      http.get(`/jobs/job-7f3a`, () => {
        jobPolls += 1;
        return HttpResponse.json(
          jobPolls < 3
            ? { ...succeededJob({ job_id: "job-7f3a" }), state: "running", rc: null }
            : succeededJob({ job_id: "job-7f3a" }),
        );
      }),
    );
    const { result } = renderHook(() => useRun(), { wrapper });

    // terminal -> the provider re-reads /status -> the board advances, poll idles
    await waitFor(() => {
      expect(statusReads).toBeGreaterThanOrEqual(2);
      const s = result.current.status;
      expect(s.status === "ready" && s.data.active_job === null).toBe(true);
      expect(result.current.activeJob.status).toBe("idle");
    });
    // the live poll really ran (two running polls + the terminal read)
    expect(jobPolls).toBeGreaterThanOrEqual(3);
    // and the refresh fired exactly once for the terminal (no re-read loop)
    await new Promise((r) => setTimeout(r, 30));
    expect(statusReads).toBe(2);
  });
});
