import "@testing-library/jest-dom/vitest";
import { afterAll, afterEach, beforeAll } from "vitest";
import { cleanup } from "@testing-library/react";

import { server } from "./handlers";

// MSW lifecycle: intercept the daemon fetch for every test, credential-free.
// "error" on unhandled requests catches a screen fetching an endpoint the test
// didn't mock (a real bug), rather than letting it hit the network.
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => {
  server.resetHandlers();
  cleanup();
});
afterAll(() => server.close());
