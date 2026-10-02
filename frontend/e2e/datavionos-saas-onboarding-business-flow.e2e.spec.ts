
import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";

async function openRegistration(page: Page) {
  await page.goto("/organization/register");
  await expect(
    page.getByRole("heading", {
      name: "Register Organization",
    }),
  ).toBeVisible();
}

test.describe(
  "DatavionOS SaaS onboarding business flow",
  () => {
    test(
      "registration page exposes backend-driven business fields",
      async ({ page }) => {
        await openRegistration(page);

        await expect(
          page.getByTestId(
            "organization-register-form",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId("organization-name"),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-admin-email",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId("organization-type"),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-category",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-size",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-country",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-state",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-district",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-city",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-address-line-1",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "organization-postal-code",
          ),
        ).toBeVisible();

        await expect(
          page.getByTestId(
            "detect-current-location",
          ),
        ).toBeVisible();
      },
    );

    test(
      "subscription plan selection is backend-driven",
      async ({ page }) => {
        await openRegistration(page);

        const planButtons =
          page.locator(
            '[data-testid^="subscription-plan-"]',
          );

        await expect(
          planButtons.first(),
        ).toBeVisible();
      },
    );

    test(
      "registration form is submit-capable",
      async ({ page }) => {
        await openRegistration(page);

        await page
          .getByTestId("organization-name")
          .fill("Datavion E2E Organization");

        await page
          .getByTestId(
            "organization-admin-email",
          )
          .fill(
            "e2e@datavionos.local",
          );

        const submit =
          page.getByTestId(
            "organization-register-submit",
          );

        await expect(submit).toBeEnabled();
        await expect(
          submit,
        ).toContainText(
          "Register Organization",
        );
      },
    );

    test(
      "login route remains reachable",
      async ({ page }) => {
        await page.goto("/login");

        await expect(
          page.getByRole("heading", {
            name: /sign in/i,
          }),
        ).toBeVisible();
      },
    );

    test(
      "registration success route remains reachable",
      async ({ page }) => {
        await page.goto(
          "/register/success?status=success",
        );

        await expect(
          page.locator("body"),
        ).toContainText(/success/i);
      },
    );
  },
);
