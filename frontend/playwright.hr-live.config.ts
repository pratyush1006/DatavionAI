import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e", testMatch: "hr.live.spec.ts", workers: 1,
  timeout: 240_000, expect: { timeout: 30_000 }, reporter: "line",
  use: { baseURL: "http://localhost:3000", ...devices["Desktop Chrome"] },
});
