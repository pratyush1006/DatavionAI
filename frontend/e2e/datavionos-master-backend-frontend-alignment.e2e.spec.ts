import { test, expect } from "@playwright/test";

test.describe(
  "DatavionOS Backend -> Frontend Alignment",
  () => {
    test(
      "frontend root responds",
      async ({ page }) => {
        const response = await page.goto("/");

        expect(response).not.toBeNull();
        expect(response?.ok()).toBeTruthy();
      },
    );

    test(
      "organization registration route responds",
      async ({ page }) => {
        const response = await page.goto(
          "/organization/register",
        );

        expect(response).not.toBeNull();
        expect(response?.ok()).toBeTruthy();
      },
    );
  },
);
