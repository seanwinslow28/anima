import { render } from "@testing-library/react";
import type { ReactElement } from "react";
import { MemoryRouter } from "react-router-dom";

// Opt into the v7 router behaviors so tests (and the app) run warning-free and
// match production routing semantics.
export const ROUTER_FUTURE = {
  v7_startTransition: true,
  v7_relativeSplatPath: true,
} as const;

/** Render a component inside a MemoryRouter at `route`. */
export function renderApp(ui: ReactElement, { route = "/" }: { route?: string } = {}) {
  return render(
    <MemoryRouter initialEntries={[route]} future={ROUTER_FUTURE}>
      {ui}
    </MemoryRouter>,
  );
}
