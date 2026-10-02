import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e", testMatch: /(hr|nurse|pharmacy|diagnostics|operations)\.e2e\.spec\.ts$/, workers: 1,
  timeout: 60_000, reporter: "line",
  expect: { timeout: 20_000 },
  use: { baseURL: "http://localhost:3000", trace: "retain-on-failure", ...devices["Desktop Chrome"] },
  webServer: {
    command: "npm.cmd run dev -- --hostname 127.0.0.1 --port 3000",
    url: "http://localhost:3000", timeout: 180_000, reuseExistingServer: true,
    env: { NEXT_PUBLIC_API_BASE_URL: "http://127.0.0.1:8000/api" },
  },
});
