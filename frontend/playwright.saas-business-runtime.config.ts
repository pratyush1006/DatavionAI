
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e-saas-business-runtime",
  testMatch: "**/*.e2e.spec.ts",

  timeout: 60_000,
  expect: {
    timeout: 10_000,
  },

  fullyParallel: false,
  workers: 1,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,

  reporter: [
    ["line"],
    ["html", {
      outputFolder: "playwright-report-saas-business-runtime",
      open: "never",
    }],
  ],

  use: {
    baseURL: "http://127.0.0.1:3001",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    ...devices["Desktop Chrome"],
  },

  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
      },
    },
  ],

  webServer: {
    command:
      "npm run start -- --hostname 127.0.0.1 --port 3001",
    url: "http://127.0.0.1:3001",
    timeout: 180_000,
    reuseExistingServer: false,
  },
});
