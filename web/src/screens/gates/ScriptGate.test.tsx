import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { ScriptGate } from "./ScriptGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import {
  beatsFixture,
  scriptMd,
  statusApproveScript,
  statusDone,
} from "../../test/fixtures";
import {
  failedJob,
  gateAccepted,
  gateBusy,
  JOB_ID,
  jobLifecycle,
  succeededJob,
} from "../../test/jobHandlers";

/*
 * The Script gate (U4a) — Sam's script.md as the screenplay lit page, the
 * INSTANT Script ⇄ Beats toggle (both artifacts fetched once, client-side
 * view state, no reload), and the honest read states: loading skeleton,
 * a 404 script (a back-compat run has none) as "no script for this run".
 * The approve flow rides U3's useGateAction — covered in its own block.
 */

const RUN = "2026-07-03-spark-tidepool";
const APPROVE = `/runs/${RUN}/script/approve`;

/** The script gate's terminal: the run advances to the storyboard gate. */
const scriptApproved = () =>
  succeededJob({
    logs: "script approved\n",
    fresh_state: { stage: "STORYBOARD" },
    next_action: { kind: "approve_storyboard", hint: "next: --approve-storyboard" },
  });

function artifactHandlers() {
  const hits = { script: 0, beats: 0 };
  server.use(
    http.get(`/runs/${RUN}/artifacts/script`, () => {
      hits.script += 1;
      return HttpResponse.text(scriptMd, {
        headers: { "Content-Type": "text/markdown; charset=utf-8" },
      });
    }),
    http.get(`/runs/${RUN}/artifacts/beats`, () => {
      hits.beats += 1;
      return HttpResponse.json(beatsFixture);
    }),
  );
  return hits;
}

function mount(status = statusApproveScript) {
  server.use(http.get("/runs/:id/status", () => HttpResponse.json(status)));
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/script`]} future={ROUTER_FUTURE}>
      <Routes>
        <Route
          path="/runs/:id"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <div data-testid="overview-screen" />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/script"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <ScriptGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route
          path="/runs/:id/storyboard"
          element={<div data-testid="storyboard-screen" />}
        />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeTheScript() {
  await waitFor(() =>
    expect(screen.getByText(/INT\. THE STUDIO — NIGHT/)).toBeInTheDocument(),
  );
}

describe("ScriptGate — the read", () => {
  it("renders the script as the default view on the lit page, ONE h1, Sam's byline", async () => {
    artifactHandlers();
    mount();
    await seeTheScript();
    // action line became prose
    expect(screen.getByText(/box-head tilted/)).toBeInTheDocument();
    // the beats view is not on stage
    expect(screen.queryByText(/calm focus/)).toBeNull();
    // one h1 — the gate title
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByText(/authored by Sam/i)).toBeInTheDocument();
    // the run's slug is stamped on the page
    expect(screen.getByText(/SCRIPT · SPARK-TIDEPOOL/)).toBeInTheDocument();
  });

  it("shows the loading skeleton while the artifacts are in flight", () => {
    artifactHandlers();
    mount();
    expect(screen.getByTestId("gate-skeleton")).toBeInTheDocument();
  });

  it("the Script ⇄ Beats toggle is instant view state — both fetched ONCE, no reload", async () => {
    const hits = artifactHandlers();
    mount();
    await seeTheScript();

    const scriptBtn = screen.getByRole("button", { name: /^script$/i });
    const beatsBtn = screen.getByRole("button", { name: /^beats$/i });
    expect(scriptBtn).toHaveAttribute("aria-pressed", "true");
    expect(beatsBtn).toHaveAttribute("aria-pressed", "false");

    // -> BEATS: the structured sheet, script off stage, INSTANTLY
    await userEvent.click(beatsBtn);
    expect(screen.getByText(/Sean draws; the mascot notices/)).toBeInTheDocument();
    expect(screen.getByText("Establishing two-shot")).toBeInTheDocument();
    expect(screen.queryByText(/INT\. THE STUDIO — NIGHT/)).toBeNull();
    expect(beatsBtn).toHaveAttribute("aria-pressed", "true");
    expect(scriptBtn).toHaveAttribute("aria-pressed", "false");

    // -> back to SCRIPT
    await userEvent.click(scriptBtn);
    expect(screen.getByText(/INT\. THE STUDIO — NIGHT/)).toBeInTheDocument();
    expect(screen.queryByText("Establishing two-shot")).toBeNull();

    // the whole dance cost exactly one fetch per artifact
    expect(hits.script).toBe(1);
    expect(hits.beats).toBe(1);
  });

  it("a 404 script (back-compat run) reads as an honest 'no script for this run'", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/script`, () =>
        HttpResponse.json({ detail: `no artifact 'script' for run '${RUN}'` }, { status: 404 }),
      ),
      http.get(`/runs/${RUN}/artifacts/beats`, () =>
        HttpResponse.json({ detail: `no artifact 'beats' for run '${RUN}'` }, { status: 404 }),
      ),
    );
    mount();
    await waitFor(() =>
      expect(screen.getByText(/no script for this run/i)).toBeInTheDocument(),
    );
    // honest, not a crash — and the recovery action is there
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("blocked_by_job disables the approve control (single-writer made visible)", async () => {
    server.use(
      http.get("/jobs/job-owner", () =>
        HttpResponse.json({
          ...succeededJob({ job_id: "job-owner" }),
          state: "running",
          rc: null,
        }),
      ),
    );
    artifactHandlers();
    mount({
      ...statusApproveScript,
      next_action: {
        kind: "approve_script",
        hint: "next: --approve-script",
        blocked_by_job: "job-owner",
      },
      active_job: { job_id: "job-owner", mutation_status: "running" },
    });
    await seeTheScript();
    expect(
      screen.getByRole("button", { name: /approve — print it/i }),
    ).toBeDisabled();
  });

  it("a non-404 artifact failure is the generic honest error with Retry", async () => {
    server.use(
      http.get(`/runs/${RUN}/artifacts/script`, () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 }),
      ),
      http.get(`/runs/${RUN}/artifacts/beats`, () => HttpResponse.json(beatsFixture)),
    );
    mount();
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the script/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("a DONE run renders the script as a PRINTED archival record with no live primary", async () => {
    artifactHandlers();
    mount(statusDone);
    await seeTheScript();
    expect(screen.getByText(/^printed$/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /approve — print it/i }),
    ).toBeNull();
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
  });
});

describe("ScriptGate — approve -> leader -> terminal (U3's hook, wired)", () => {
  it("approve runs the leader, then ADVANCES on the inline next_action to the storyboard gate", async () => {
    artifactHandlers();
    mount();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, scriptApproved(), 3));
    await seeTheScript();
    // the ONE decision (density gate: the script + one approve)
    const approve = screen.getByRole("button", { name: /approve — print it/i });
    expect(approve).toBeEnabled();
    await userEvent.click(approve);
    // the shared ritual leader is the working state
    await waitFor(() => expect(screen.getByRole("status")).toBeInTheDocument());
    // terminal (succeeded, next_action approve_storyboard) -> the storyboard route
    await waitFor(() =>
      expect(screen.getByTestId("storyboard-screen")).toBeInTheDocument(),
    );
  });

  it("⌘⏎ approves (keyboard is a first-class hand)", async () => {
    artifactHandlers();
    mount();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, scriptApproved(), 2));
    await seeTheScript();
    await userEvent.keyboard("{Meta>}{Enter}{/Meta}");
    await waitFor(() =>
      expect(screen.getByTestId("storyboard-screen")).toBeInTheDocument(),
    );
  });

  it("failed (rc != 0) surfaces rc + the logs tail honestly, with Retry — no advance", async () => {
    artifactHandlers();
    mount();
    server.use(
      gateAccepted(APPROVE),
      jobLifecycle(
        JOB_ID,
        failedJob({ rc: 2, logs: "beats.json failed the structural pass\n" }),
        1,
      ),
    );
    await seeTheScript();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() =>
      expect(screen.getByText(/jammed in the gate/i)).toBeInTheDocument(),
    );
    expect(screen.getByText(/rc 2/)).toBeInTheDocument();
    expect(screen.getByText(/structural pass/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
    expect(screen.queryByTestId("storyboard-screen")).toBeNull();
  });

  it("409-busy offers to watch the running job", async () => {
    artifactHandlers();
    mount();
    server.use(gateBusy(APPROVE, "job-owner"));
    await seeTheScript();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() => expect(screen.getByText(/booth is busy/i)).toBeInTheDocument());
    expect(
      screen.getByRole("link", { name: /watch the running job/i }),
    ).toHaveAttribute("href", `/runs/${RUN}`);
  });
});
