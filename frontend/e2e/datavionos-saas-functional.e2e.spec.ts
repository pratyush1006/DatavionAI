import { expect, test } from "@playwright/test";

const PUBLIC_ROUTES = [
  "/",
  "/about",
  "/careers",
  "/case-studies",
  "/features",
  "/pricing",
  "/support",
] as const;

const AUTH_ROUTES = [
  "/login",
  "/register",
  "/forgot-password",
] as const;

const ORGANIZATION_ROUTES = [
  "/organization",
  "/organization/register",
  "/organization/modules",
  "/organization/subscription",
] as const;

const DASHBOARD_ROUTES = [
  "/dashboard",
  "/settings/access",
  "/settings/ai",
  "/settings/modules",
] as const;

const WORKSPACE_ROUTES = [
  "/patients",
  "/documents",
  "/documents/new",
  "/employees",
  "/notes",
  "/transcription",
  "/clinical/appointments",
] as const;

const ALL_NAVIGATION_ROUTES = [
  ...PUBLIC_ROUTES,
  ...AUTH_ROUTES,
  ...ORGANIZATION_ROUTES,
  ...DASHBOARD_ROUTES,
  ...WORKSPACE_ROUTES,
] as const;


/*
 * IMPORTANT ARCHITECTURAL RULE
 * -----------------------------
 *
 * Do not type this helper as a generated Next.js Route union.
 *
 * Next.js generates an internal route type from the application tree.
 * Playwright E2E tests intentionally operate on runtime URL strings.
 *
 * Therefore this helper accepts `string`.
 *
 * This prevents the TS2345 failure:
 *
 *   Argument of type 'string' is not assignable to parameter of type
 *   generated Next.js route union
 *
 * while preserving runtime route validation.
 */
async function visitRoute(
  page: Parameters<typeof test>[0] extends never ? never : any,
  route: string,
): Promise<void> {
  const response = await page.goto(route, {
    waitUntil: "domcontentloaded",
    timeout: 30_000,
  });

  expect(response).not.toBeNull();

  if (response) {
    expect(response.status()).toBeLessThan(500);
  }
}


async function assertRouteAvailable(
  page: any,
  route: string,
): Promise<void> {
  await visitRoute(page, route);

  await expect(page.locator("body")).toBeVisible();

  const bodyText = (await page.locator("body").innerText()).trim();

  expect(bodyText.length).toBeGreaterThan(0);
}


test.describe("DatavionOS SaaS functional runtime", () => {
  test.describe.configure({
    mode: "serial",
  });

  test("public routes render successfully", async ({ page }) => {
    for (const route of PUBLIC_ROUTES) {
      await assertRouteAvailable(page, route);
    }
  });

  test("authentication routes render successfully", async ({ page }) => {
    for (const route of AUTH_ROUTES) {
      await assertRouteAvailable(page, route);
    }
  });

  test("sign-in links to the password recovery flow", async ({ page }) => {
    await visitRoute(page, "/login");

    const recoveryLink = page.getByRole("link", {
      name: "Forgot password?",
    });
    await expect(recoveryLink).toHaveAttribute("href", "/forgot-password");
    await recoveryLink.click();

    await expect(page).toHaveURL(/\/forgot-password$/);
    await expect(page.getByText("Forgot your password?", { exact: true })).toBeVisible();
  });

  test("sign-in uses the mounted authentication API route", async ({ page }) => {
    await page.route("**/api/auth/login/", async (route) => {
      await route.fulfill({
        status: 401,
        contentType: "application/json",
        body: JSON.stringify({
          success: false,
          error: {
            code: "UNAUTHENTICATED",
            message: "Invalid email or password.",
            details: null,
          },
          meta: { api_version: "v1" },
        }),
      });
    });

    await visitRoute(page, "/login");
    await page.getByLabel("Email").fill("invalid@example.test");
    await page.getByLabel("Password").fill("InvalidPassword2026");

    const loginRequest = page.waitForRequest(
      (request) =>
        request.method() === "POST" &&
        new URL(request.url()).pathname === "/api/auth/login/",
    );
    await page.getByRole("button", { name: "Sign In" }).click();
    await loginRequest;

    await expect(
      page.getByRole("alert").filter({
        hasText: "Invalid email or password.",
      }),
    ).toBeVisible();
  });

  test("organization routes render successfully", async ({ page }) => {
    for (const route of ORGANIZATION_ROUTES) {
      await assertRouteAvailable(page, route);
    }
  });

  test("dashboard and workspace routes render successfully", async ({ page }) => {
    for (const route of DASHBOARD_ROUTES) {
      await assertRouteAvailable(page, route);
    }

    for (const route of WORKSPACE_ROUTES) {
      await assertRouteAvailable(page, route);
    }
  });

  test("navigation links expose valid internal destinations", async ({ page }) => {
    await visitRoute(page, "/");

    const links = page.locator("a[href]");
    const count = await links.count();

    expect(count).toBeGreaterThan(0);

    const hrefs = new Set<string>();

    for (let index = 0; index < count; index += 1) {
      const href = await links.nth(index).getAttribute("href");

      if (typeof href !== "string" || href.trim() === "") {
        continue;
      }

      hrefs.add(href);
    }

    expect(hrefs.size).toBeGreaterThan(0);

    for (const href of hrefs) {
      if (
        href.startsWith("/") &&
        !href.startsWith("//") &&
        !href.startsWith("/api/")
      ) {
        const response = await page.goto(href, {
          waitUntil: "domcontentloaded",
          timeout: 30_000,
        });

        expect(response).not.toBeNull();

        if (response) {
          expect(response.status()).toBeLessThan(500);
        }

        await expect(page.locator("body")).toBeVisible();
      }
    }
  });
});
