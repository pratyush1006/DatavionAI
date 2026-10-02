import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  testMatch: "**/*.e2e.spec.ts",

  fullyParallel: false,
  forbidOnly: !!process.env.CI,

  retries: process.env.CI ? 2 : 0,
  workers: 1,

  timeout: 60_000,

  reporter: process.env.CI ? "line" : "html",

  webServer: {
    command: "npm run start -- --hostname 127.0.0.1 --port 3001",
    url: "http://127.0.0.1:3001",
    timeout: 180_000,
    reuseExistingServer: false,
    stdout: "pipe",
    stderr: "pipe",
  },

  use: {
    baseURL:
      process.env.DATAVIONOS_DASHBOARD_URL ??
      "http://127.0.0.1:3001",

    trace: "on-first-retry",

    navigationTimeout: 30_000,
    actionTimeout: 15_000,

    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
      },
    },
  ],
});
