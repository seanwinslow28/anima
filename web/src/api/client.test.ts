import { http, HttpResponse } from "msw";
import { describe, expect, it } from "vitest";

import { fetchArtifact, fetchJob, postGate } from "./client";
import type { GateAction } from "./types";
import { isTerminalJobState } from "./types";
import {
  gateAccepted,
  gateBusy,
  gateError,
  gateStale,
  JOB_ID,
  jobGone,
  jobLifecycle,
  succeededJob,
} from "../test/jobHandlers";
import { server } from "../test/handlers";

const RUN = "2026-07-03-spark-tidepool";
const APPROVE = `/runs/${RUN}/plan/approve`;
const action: GateAction = { method: "POST", path: APPROVE };

describe("postGate — the four POST outcomes, discriminated", () => {
  it("202 -> accepted with the job id", async () => {
    server.use(gateAccepted(APPROVE));
    expect(await postGate(action)).toEqual({ kind: "accepted", jobId: JOB_ID });
  });

  it("409 with a dict detail -> busy (active_job_id + reason)", async () => {
    server.use(gateBusy(APPROVE, "job-elsewhere"));
    expect(await postGate(action)).toEqual({
      kind: "busy",
      activeJobId: "job-elsewhere",
      reason: "a job already owns this run",
    });
  });

  it("409 with a plain-string detail -> stale, NOT busy", async () => {
    server.use(gateStale(APPROVE, "run is at stage 'SCRIPT', not 'PLAN' (this gate's stage)"));
    expect(await postGate(action)).toEqual({
      kind: "stale",
      detail: "run is at stage 'SCRIPT', not 'PLAN' (this gate's stage)",
    });
  });

  it("404 -> error carrying status + detail", async () => {
    server.use(gateError(APPROVE, 404, `no run '${RUN}'`));
    expect(await postGate(action)).toEqual({
      kind: "error",
      status: 404,
      detail: `no run '${RUN}'`,
    });
  });

  it("422 -> error carrying status + detail", async () => {
    server.use(gateError(APPROVE, 422, "retry requires a non-empty note"));
    expect(await postGate(action)).toEqual({
      kind: "error",
      status: 422,
      detail: "retry requires a non-empty note",
    });
  });

  it("a non-string error detail (Pydantic 422 array) is stringified, never [object Object]", async () => {
    server.use(
      http.post(APPROVE, () =>
        HttpResponse.json(
          { detail: [{ loc: ["body", "note"], msg: "field required" }] },
          { status: 422 },
        ),
      ),
    );
    const result = await postGate(action);
    expect(result.kind).toBe("error");
    if (result.kind === "error") {
      expect(result.detail).toContain("field required");
      expect(result.detail).not.toContain("[object Object]");
    }
  });

  it("sends a JSON body when the action carries one (U5 retry note)", async () => {
    let received: unknown = null;
    server.use(
      http.post(`/runs/${RUN}/frames/3/retry`, async ({ request }) => {
        received = await request.json();
        return HttpResponse.json({ job_id: JOB_ID }, { status: 202 });
      }),
    );
    const retry: GateAction = {
      method: "POST",
      path: `/runs/${RUN}/frames/3/retry`,
      body: { note: "hold the silhouette" },
    };
    expect(await postGate(retry)).toEqual({ kind: "accepted", jobId: JOB_ID });
    expect(received).toEqual({ note: "hold the silhouette" });
  });
});

describe("fetchJob", () => {
  it("returns the JobView (running, then the terminal on a later poll)", async () => {
    server.use(jobLifecycle(JOB_ID, succeededJob(), 1));
    const first = await fetchJob(JOB_ID);
    expect(first.state).toBe("running");
    expect(isTerminalJobState(first.state)).toBe(false);
    const second = await fetchJob(JOB_ID);
    expect(second.state).toBe("succeeded");
    expect(second.rc).toBe(0);
    expect(second.next_action?.kind).toBe("approve_script");
    expect(isTerminalJobState(second.state)).toBe(true);
  });

  it("throws on 404 (daemon restarted — job registry is process-lifetime)", async () => {
    server.use(jobGone("job-lost"));
    await expect(fetchJob("job-lost")).rejects.toThrow(/404/);
  });
});

describe("fetchArtifact", () => {
  it("returns the artifact text (plan.md as text/markdown)", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/plan`, () =>
        HttpResponse.text("# The Plan\n\nMaya's prose.", {
          headers: { "Content-Type": "text/markdown; charset=utf-8" },
        }),
      ),
    );
    expect(await fetchArtifact(RUN, "plan")).toBe("# The Plan\n\nMaya's prose.");
  });

  it("throws on 404 (no artifact yet)", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/plan`, () =>
        HttpResponse.json({ detail: "no artifact 'plan'" }, { status: 404 }),
      ),
    );
    await expect(fetchArtifact(RUN, "plan")).rejects.toThrow(/404/);
  });
});
