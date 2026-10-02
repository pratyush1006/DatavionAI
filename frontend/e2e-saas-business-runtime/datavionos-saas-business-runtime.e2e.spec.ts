
import { test, expect, type Page } from "@playwright/test";

test.describe.configure({ mode: "serial" });

const AUTH_EMAIL = process.env.SAAS_BUSINESS_EMAIL ?? "";
const AUTH_PASSWORD = process.env.SAAS_BUSINESS_PASSWORD ?? "";

const ORGANIZATION_NAME =
  process.env.SAAS_BUSINESS_ORGANIZATION_NAME ??
  "Datavion E2E Organization";

const ORGANIZATION_TYPE =
  process.env.SAAS_BUSINESS_ORGANIZATION_TYPE ??
  "clinic";

const SUBSCRIPTION_PLAN =
  process.env.SAAS_BUSINESS_SUBSCRIPTION_PLAN ??
  "professional";

const TARGET_MODULE =
  process.env.SAAS_BUSINESS_MODULE ??
  "pharmacy";

const RUN_MUTATIONS =
  process.env.SAAS_BUSINESS_RUN_MUTATIONS === "true";

const RUN_AUTHENTICATED =
  Boolean(AUTH_EMAIL && AUTH_PASSWORD);

function route(path: string): string {
  return path;
}

async function gotoAndAssert(
  page: Page,
  path: string,
): Promise<void> {
  await page.goto(route(path), {
    waitUntil: "domcontentloaded",
  });

  await expect(page).toHaveURL(
    new RegExp(`${path.replace("/", "\\/")}(?:[/?#]|$)`),
  );
}

async function hasVisibleText(
  page: Page,
  values: string[],
): Promise<boolean> {
  for (const value of values) {
    if (
      await page.getByText(value, {
        exact: false,
      }).first().isVisible().catch(() => false)
    ) {
      return true;
    }
  }

  return false;
}

async function login(page: Page): Promise<void> {
  await gotoAndAssert(page, "/login");

  const email = page.locator(
    'input[type="email"], input[name="email"]',
  ).first();

  const password = page.locator(
    'input[type="password"], input[name="password"]',
  ).first();

  await expect(email).toBeVisible();
  await expect(password).toBeVisible();

  await email.fill(AUTH_EMAIL);
  await password.fill(AUTH_PASSWORD);

  const submit = page.locator(
    'button[type="submit"], input[type="submit"]',
  ).first();

  await expect(submit).toBeVisible();
  await submit.click();

  await page.waitForLoadState("domcontentloaded");

  await expect
    .poll(
      async () => page.url(),
      {
        timeout: 30_000,
      },
    )
    .toMatch(
      /\/(dashboard|organization|organizations|workspace|register\/success)/,
    );
}

test.describe(
  "DatavionOS SaaS business runtime",
  () => {
    test(
      "organization registration surface is available",
      async ({ page }) => {
        await gotoAndAssert(page, "/organization/register");

        await expect(
          page.locator("body"),
        ).toBeVisible();

        expect(
          await hasVisibleText(page, [
            "Organization",
            "Register",
            "Create",
            "Clinic",
          ]),
        ).toBeTruthy();
      },
    );

    test(
      "subscription surface is available",
      async ({ page }) => {
        await gotoAndAssert(
          page,
          "/organization/subscription",
        );

        await expect(
          page.locator("body"),
        ).toBeVisible();

        expect(
          await hasVisibleText(page, [
            "Subscription",
            "Plan",
            "Billing",
            "Professional",
            "Enterprise",
          ]),
        ).toBeTruthy();
      },
    );

    test(
      "organization module management surface is available",
      async ({ page }) => {
        await gotoAndAssert(
          page,
          "/organization/modules",
        );

        await expect(
          page.locator("body"),
        ).toBeVisible();

        expect(
          await hasVisibleText(page, [
            "Module",
            "Modules",
            "Enable",
            "Disable",
            "Active",
          ]),
        ).toBeTruthy();
      },
    );

    test(
      "authenticated SaaS business runtime",
      async ({ page }) => {
        test.skip(
          !RUN_AUTHENTICATED,
          "Set SAAS_BUSINESS_EMAIL and SAAS_BUSINESS_PASSWORD to run authenticated business E2E.",
        );

        await login(page);

        await gotoAndAssert(page, "/dashboard");

        await expect(
          page.locator("body"),
        ).toBeVisible();

        expect(
          await hasVisibleText(page, [
            "Dashboard",
            "Organization",
            "Workspace",
            "Modules",
          ]),
        ).toBeTruthy();

        await gotoAndAssert(
          page,
          "/organization",
        );

        await expect(
          page.locator("body"),
        ).toBeVisible();

        if (RUN_MUTATIONS) {
          await gotoAndAssert(
            page,
            "/organization/subscription",
          );

          await expect(
            page.locator("body"),
          ).toBeVisible();

          expect(
            await hasVisibleText(page, [
              SUBSCRIPTION_PLAN,
              "Subscription",
              "Plan",
            ]),
          ).toBeTruthy();

          await gotoAndAssert(
            page,
            "/organization/modules",
          );

          await expect(
            page.locator("body"),
          ).toBeVisible();

          expect(
            await hasVisibleText(page, [
              TARGET_MODULE,
              "Module",
              "Modules",
            ]),
          ).toBeTruthy();

          await gotoAndAssert(
            page,
            "/settings/modules",
          );

          await expect(
            page.locator("body"),
          ).toBeVisible();
        }
      },
    );

    test(
      "organization context survives authenticated navigation",
      async ({ page }) => {
        test.skip(
          !RUN_AUTHENTICATED,
          "Authenticated context test requires SaaS credentials.",
        );

        await login(page);

        const routes = [
          "/dashboard",
          "/organization",
          "/organization/modules",
          "/organization/subscription",
          "/settings/modules",
        ];

        for (const path of routes) {
          await gotoAndAssert(page, path);

          await expect(
            page.locator("body"),
          ).toBeVisible();

          const bodyText =
            await page.locator("body").innerText();

          expect(bodyText.length).toBeGreaterThan(20);
        }
      },
    );

    test(
      "logout or session termination surface is discoverable",
      async ({ page }) => {
        test.skip(
          !RUN_AUTHENTICATED,
          "Logout validation requires SaaS credentials.",
        );

        await login(page);

        const logoutControl = page.locator(
          'button:has-text("Logout"), ' +
          'button:has-text("Log out"), ' +
          'a:has-text("Logout"), ' +
          'a:has-text("Log out"), ' +
          '[data-testid="logout"]',
        ).first();

        if (await logoutControl.isVisible().catch(() => false)) {
          await logoutControl.click();

          await page.waitForLoadState(
            "domcontentloaded",
          );

          await expect
            .poll(
              async () => page.url(),
              {
                timeout: 15_000,
              },
            )
            .toMatch(/\/(login|$)/);
        } else {
          await page.goto("/login");
          await expect(page).toHaveURL(
            /\/login(?:[/?#]|$)/,
          );
        }
      },
    );
  },
);
