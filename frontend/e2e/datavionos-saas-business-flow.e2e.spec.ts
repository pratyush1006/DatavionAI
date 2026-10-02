import { test, expect, type Page } from "@playwright/test";

const BASE_URL = "http://127.0.0.1:3001";

async function assertPageRenders(page: Page, path: string) {
  await page.goto(`${BASE_URL}${path}`, {
    waitUntil: "domcontentloaded",
  });

  await expect(page.locator("body")).toBeVisible();
}

test.describe("DatavionOS SaaS business flow", () => {
  test("registration form exposes the canonical business contract", async ({
    page,
  }) => {
    await page.goto(`${BASE_URL}/organization/register`, {
      waitUntil: "domcontentloaded",
    });

    await expect(
      page.getByTestId("organization-register-form"),
    ).toBeVisible();

    await expect(
      page.getByTestId("organization-name"),
    ).toBeVisible();

    await expect(
      page.getByTestId("organization-type"),
    ).toBeVisible();

    await expect(
      page.getByTestId("subscription-plan"),
    ).toBeVisible();

    await expect(
      page.getByTestId("organization-admin-email"),
    ).toBeVisible();

    await expect(
      page.getByTestId("organization-register-submit"),
    ).toBeVisible();

    await expect(
      page.getByRole("heading", {
        name: "Register Organization",
      }),
    ).toBeVisible();

    const organizationTypeOptions = page
      .getByTestId("organization-type")
      .locator("option");

    await expect(organizationTypeOptions).toHaveCount(4);

    await expect(
      page.getByTestId("organization-type"),
    ).toContainText([
      "Clinic",
      "Hospital",
      "Pharmacy",
      "Laboratory",
    ]);

    const subscriptionOptions = page
      .getByTestId("subscription-plan")
      .locator("option");

    await expect(subscriptionOptions).toHaveCount(3);

    await expect(
      page.getByTestId("subscription-plan"),
    ).toContainText([
      "Starter",
      "Professional",
      "Enterprise",
    ]);
  });

  test("organization registration submits and reaches success", async ({
    page,
  }) => {
    await page.goto(`${BASE_URL}/organization/register`, {
      waitUntil: "domcontentloaded",
    });

    await page.getByTestId("organization-name").fill(
      "Datavion E2E Clinic",
    );

    await page.getByTestId("organization-type").selectOption(
      "clinic",
    );

    await page.getByTestId("subscription-plan").selectOption(
      "professional",
    );

    await page.getByTestId("organization-admin-email").fill(
      "e2e@datavion.local",
    );

    await page.getByTestId(
      "organization-register-submit",
    ).click();

    await expect(page).toHaveURL(
      /\/register\/success(?:[/?#]|$)/,
    );

    await expect(page.locator("body")).toContainText(
      /success|registered|organization/i,
    );
  });

  test("authentication route remains reachable", async ({
    page,
  }) => {
    await assertPageRenders(page, "/login");

    await expect(
      page.getByRole("button", {
        name: /sign in/i,
      }),
    ).toBeVisible();
  });

  test("organization context route remains reachable", async ({
    page,
  }) => {
    await assertPageRenders(page, "/organization");
  });

  test("subscription state route remains reachable", async ({
    page,
  }) => {
    await assertPageRenders(
      page,
      "/organization/subscription",
    );
  });

  test("module state route remains reachable", async ({
    page,
  }) => {
    await assertPageRenders(
      page,
      "/organization/modules",
    );
  });

  test("dynamic dashboard remains reachable", async ({
    page,
  }) => {
    await assertPageRenders(page, "/dashboard");
  });

  test("organization module controls remain discoverable", async ({
    page,
  }) => {
    await page.goto(
      `${BASE_URL}/organization/modules`,
      {
        waitUntil: "domcontentloaded",
      },
    );

    await expect(page.locator("body")).toBeVisible();

    const interactiveElements = page.locator(
      "button, input, select, a",
    );

    const count = await interactiveElements.count();

    expect(count).toBeGreaterThan(0);
  });

  test("business flow routes remain internally navigable", async ({
    page,
  }) => {
    const routes = [
      "/organization/register",
      "/register/success",
      "/login",
      "/organization",
      "/organization/subscription",
      "/organization/modules",
      "/dashboard",
    ];

    for (const route of routes) {
      await assertPageRenders(page, route);
    }
  });
});
