import { screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import App from "./App";
import { renderApp } from "./test/render";

describe("app shell", () => {
  it("renders the anima wordmark and a main landmark", () => {
    renderApp(<App />, { route: "/" });

    // The wordmark is a real navigation control (a11y contract), home is "/".
    expect(screen.getByRole("link", { name: /anima/i })).toBeInTheDocument();
    // One <main> landmark per screen.
    expect(screen.getByRole("main")).toBeInTheDocument();
  });
});
