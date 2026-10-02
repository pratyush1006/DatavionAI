import { defineConfig, devices } from "@playwright/test";

const dashboardUrl =
  process.env.DATAVIONOS_DASHBOARD_URL ?? "http://127.0.0.1:3001";

export default defineConfig({
  testDir: "./e2e",
  testMatch: "datavionos-organization-registration-details.e2e.spec.ts",
  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  timeout: 120_000,
  expect: {
    timeout: 15_000,
  },
  reporter: "line",
  use: {
    baseURL: dashboardUrl,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    ...devices["Desktop Chrome"],
  },
  webServer: [
    {
      command: "python manage.py runserver 127.0.0.1:8000",
      cwd: "../backend",
      url: "http://127.0.0.1:8000/api/onboarding/catalog/",
      timeout: 180_000,
      reuseExistingServer: !process.env.CI,
      stdout: "pipe",
      stderr: "pipe",
    },
    {
      command: "npm run start -- --hostname 127.0.0.1 --port 3001",
      url: dashboardUrl,
      timeout: 600_000,
      reuseExistingServer: false,
      stdout: "pipe",
      stderr: "pipe",
    },
  ],
});
