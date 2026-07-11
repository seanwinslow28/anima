import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { PlanGate } from "./PlanGate";
import { RunProvider } from "../../lib/runContext";
import { ROUTER_FUTURE } from "../../test/render";
import { server } from "../../test/handlers";
import {
  rawAuthoring,
  statusApprovePlan,
  statusApprovePlanBlocked,
} from "../../test/fixtures";
import {
  degradedJob,
  failedJob,
  gateAccepted,
  gateBusy,
  gateError,
  gateStale,
  JOB_ID,
  jobLifecycle,
  succeededJob,
} from "../../test/jobHandlers";

/*
 * The Plan gate — the whole D-C flow proven on the simplest document gate:
 * the lit page (Maya's plan.md as prose) + the cost preview + ONE primary
 * action, then approve -> 202 -> leader -> terminal -> advance on the
 * inline next_action. Every non-happy branch renders an honest state.
 */

const RUN = "2026-07-03-spark-tidepool";
const APPROVE = `/runs/${RUN}/plan/approve`;
const PLAN_MD = "# Spark Tidepool\n\nA five-frame loop.\n\n- one character";

function mount(status = statusApprovePlan) {
  server.use(
    http.get("/runs/:id/status", () => HttpResponse.json(status)),
    http.get(`/runs/${RUN}/artifacts/plan`, () =>
      HttpResponse.text(PLAN_MD, {
        headers: { "Content-Type": "text/markdown; charset=utf-8" },
      }),
    ),
    http.get("/runs/:id", () => HttpResponse.json(rawAuthoring)),
  );
  return render(
    <MemoryRouter initialEntries={[`/runs/${RUN}/plan`]} future={ROUTER_FUTURE}>
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
          path="/runs/:id/plan"
          element={
            <RunProvider runId={RUN} pollIntervalMs={5}>
              <PlanGate pollIntervalMs={5} />
            </RunProvider>
          }
        />
        <Route path="/runs/:id/script" element={<div data-testid="script-screen" />} />
      </Routes>
    </MemoryRouter>,
  );
}

async function seeThePage() {
  await waitFor(() =>
    expect(screen.getByText("A five-frame loop.")).toBeInTheDocument(),
  );
}

describe("PlanGate — the read", () => {
  it("renders the plan as the lit page + the cost preview + ONE approve action", async () => {
    mount();
    await seeThePage();
    // markdown became prose (demoted heading, list item), not a <pre> dump
    expect(screen.getByRole("heading", { level: 2, name: "Spark Tidepool" })).toBeInTheDocument();
    expect(screen.getByText("one character")).toBeInTheDocument();
    // one h1 — the gate title
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    // the cost preview with the honesty label
    expect(screen.getByText(/estimate, not a cap/i)).toBeInTheDocument();
    expect(screen.getByText(/est \$0\.35 – \$2\.25/)).toBeInTheDocument();
    // the one decision
    const approve = screen.getByRole("button", { name: /approve — print it/i });
    expect(approve).toBeEnabled();
    expect(approve).toHaveClass("gate-approve", "ro-button", "ro-button--primary");
  });

  it("an unreadable plan artifact is an honest error state with a retry", async () => {
    server.use(
      http.get("/runs/:id/status", () => HttpResponse.json(statusApprovePlan)),
      http.get(`/runs/${RUN}/artifacts/plan`, () =>
        HttpResponse.json({ detail: "no artifact 'plan'" }, { status: 404 }),
      ),
      http.get("/runs/:id", () => HttpResponse.json(rawAuthoring)),
    );
    render(
      <MemoryRouter initialEntries={[`/runs/${RUN}/plan`]} future={ROUTER_FUTURE}>
        <Routes>
          <Route
            path="/runs/:id/plan"
            element={
              <RunProvider runId={RUN} pollIntervalMs={5}>
                <PlanGate pollIntervalMs={5} />
              </RunProvider>
            }
          />
        </Routes>
      </MemoryRouter>,
    );
    await waitFor(() =>
      expect(screen.getByText(/couldn't read the plan/i)).toBeInTheDocument(),
    );
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
  });

  it("blocked_by_job disables the approve control (single-writer made visible)", async () => {
    // the provider live-polls the owning job; keep it running for the test
    server.use(
      http.get("/jobs/job-owner", () =>
        HttpResponse.json({ ...succeededJob({ job_id: "job-owner" }), state: "running", rc: null }),
      ),
    );
    mount(statusApprovePlanBlocked);
    await seeThePage();
    const approve = screen.getByRole("button", { name: /approve — print it/i });
    expect(approve).toBeDisabled();
    expect(screen.getByText(/job-owner/)).toBeInTheDocument();
  });
});

describe("PlanGate — approve -> leader -> terminal", () => {
  it("approve runs the leader, then ADVANCES on the inline next_action route", async () => {
    mount();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, succeededJob(), 3));
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    // the ritual leader is the working state
    await waitFor(() => expect(screen.getByRole("status")).toBeInTheDocument());
    // terminal (succeeded, next_action approve_script) -> the script route
    await waitFor(() =>
      expect(screen.getByTestId("script-screen")).toBeInTheDocument(),
    );
  });

  it("⌘⏎ approves (keyboard is a first-class hand)", async () => {
    mount();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, succeededJob(), 2));
    await seeThePage();
    await userEvent.keyboard("{Meta>}{Enter}{/Meta}");
    await waitFor(() =>
      expect(screen.getByTestId("script-screen")).toBeInTheDocument(),
    );
  });

  it("failed (rc != 0) surfaces rc + the logs tail honestly, with Retry", async () => {
    mount();
    server.use(
      gateAccepted(APPROVE),
      jobLifecycle(JOB_ID, failedJob({ rc: 2, logs: "the gate refused: no criteria lock\n" }), 1),
    );
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() =>
      expect(screen.getByText(/jammed in the gate/i)).toBeInTheDocument(),
    );
    expect(screen.getByText(/rc 2/)).toBeInTheDocument();
    expect(screen.getByText(/no criteria lock/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
    // no auto-advance
    expect(screen.queryByTestId("script-screen")).toBeNull();
  });

  it("degraded success (rc 0 + load_error) shows the reload state, NO auto-advance", async () => {
    mount();
    server.use(gateAccepted(APPROVE), jobLifecycle(JOB_ID, degradedJob(), 1));
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() =>
      expect(screen.getByText(/couldn't re-read/i)).toBeInTheDocument(),
    );
    expect(screen.queryByTestId("script-screen")).toBeNull();
  });

  it("409-busy offers to watch the running job (not a dead 'watch' on stale)", async () => {
    mount();
    server.use(gateBusy(APPROVE, "job-owner"));
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() => expect(screen.getByText(/booth is busy/i)).toBeInTheDocument());
    const watch = screen.getByRole("link", { name: /watch the running job/i });
    expect(watch).toHaveAttribute("href", `/runs/${RUN}`);
  });

  it("409-stale says the run already moved on — refresh, NOT busy", async () => {
    mount();
    server.use(gateStale(APPROVE));
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() =>
      expect(screen.getByText(/already moved on/i)).toBeInTheDocument(),
    );
    expect(screen.queryByText(/watch the running job/i)).toBeNull();
  });

  it("422 renders the honest error state with the reason", async () => {
    mount();
    server.use(gateError(APPROVE, 422, "could not load run state"));
    await seeThePage();
    await userEvent.click(screen.getByRole("button", { name: /approve — print it/i }));
    await waitFor(() =>
      expect(screen.getByText(/could not load run state/i)).toBeInTheDocument(),
    );
  });
});
