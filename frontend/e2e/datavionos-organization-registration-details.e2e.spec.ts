import { expect, test } from "@playwright/test";
import type { Page, Response } from "@playwright/test";

const REGISTRATION_PATH = "/organization/register";
const ONBOARDING_CATALOG_PATH = "/api/onboarding/catalog/";

async function openRegistration(page: Page): Promise<Response> {
  const catalogResponse = page.waitForResponse((response) =>
    new URL(response.url()).pathname.endsWith(ONBOARDING_CATALOG_PATH),
  );

  await page.goto(REGISTRATION_PATH);
  await expect(page).toHaveURL(
    /\/organization\/register(?:[/?#]|$)/,
  );

  return catalogResponse;
}

test.describe("DatavionOS organization registration catalogs", () => {
  test("renders all eight backend organization categories", async ({
    page,
  }) => {
    const catalogResponse = await openRegistration(page);
    expect(catalogResponse.status()).toBe(200);

    const category = page.getByTestId("organization-category");
    await expect(category).toBeVisible();
    await expect(category.locator("option")).toHaveCount(9);

    for (const name of [
      "Healthcare Provider",
      "Diagnostics",
      "Pharmacy",
      "Emergency Services",
      "Insurance",
      "Research & Education",
      "Public Health",
      "Enterprise",
    ]) {
      await expect(
        category.locator("option", { hasText: name }),
      ).toHaveCount(1);
    }
  });

  test("renders all five backend organization sizes", async ({ page }) => {
    const catalogResponse = await openRegistration(page);
    expect(catalogResponse.status()).toBe(200);

    const size = page.getByTestId("organization-size");
    await expect(size).toBeVisible();
    await expect(size.locator("option")).toHaveCount(6);

    for (const name of [
      "Solo Practice",
      "Small",
      "Medium",
      "Large",
      "Enterprise",
    ]) {
      await expect(size.locator("option", { hasText: name })).toHaveCount(1);
    }
  });

  test("selecting a category filters backend organization types", async ({
    page,
  }) => {
    const catalogResponse = await openRegistration(page);
    expect(catalogResponse.status()).toBe(200);

    const category = page.getByTestId("organization-category");
    const type = page.getByTestId("organization-type");

    await category.selectOption("healthcare_provider");
    await expect(category).toHaveValue("healthcare_provider");
    await expect(type).toBeEnabled();
    await expect(type.locator('option[value="clinic"]')).toHaveCount(1);
    await expect(type.locator('option[value="laboratory"]')).toHaveCount(0);

    await type.selectOption("clinic");
    await expect(type).toHaveValue("clinic");
    await page.getByTestId("organization-size").selectOption("medium");
    await expect(page.getByTestId("organization-size")).toHaveValue("medium");
  });

  test("registers an organization through backend provisioning", async ({
    page,
  }) => {
    await openRegistration(page);

    await page.getByTestId("organization-category").selectOption("pharmacy");
    await page.getByTestId("organization-type").selectOption("retail_pharmacy");
    await page.getByTestId("organization-size").selectOption("solo");

    const plansResponsePromise = page.waitForResponse((response) =>
      new URL(response.url()).pathname.endsWith("/api/onboarding/plans/"),
    );
    await page.getByRole("button", { name: "Continue →" }).click();

    const plansResponse = await plansResponsePromise;
    expect(plansResponse.status()).toBe(200);
    const plansBody = (await plansResponse.json()) as {
      data: Array<{
        id: string;
        code: string;
        price: string;
        trial_days: number;
      }>;
    };
    const eligiblePlan = plansBody.data.find(
      (plan) => Number(plan.price) === 0 || plan.trial_days > 0,
    );
    expect(eligiblePlan, "a signup-eligible plan is available").toBeDefined();
    if (!eligiblePlan) {
      throw new Error("No signup-eligible plan was returned by the backend.");
    }

    await page.getByTestId(`signup-plan-${eligiblePlan.id}`).click();
    const preflightResponsePromise = page.waitForResponse((response) =>
      new URL(response.url()).pathname.endsWith("/api/onboarding/signup/preflight/"),
    );
    await page.getByRole("button", { name: "Continue →" }).click();
    expect((await preflightResponsePromise).status()).toBe(200);

    const uniqueId = `${Date.now()}-${Math.floor(Math.random() * 1_000_000)}`;
    const organizationName = `Datavion E2E Pharmacy ${uniqueId}`;
    const email = `datavion-e2e-${uniqueId}@example.test`;

    await page.getByLabel("Organization name").fill(organizationName);
    await page.getByLabel("Display name").fill(organizationName);
    await page.getByLabel("Primary organization email").fill(email);
    await page.getByRole("button", { name: "Continue →" }).click();

    await page.getByLabel("First name").fill("E2E");
    await page.getByLabel("Last name").fill("Owner");
    await page.getByLabel("Administrator email").fill(email);
    await page.getByLabel("Password").fill("Saffron!Secure-Workspace-2026");
    await page.getByRole("button", { name: "Continue →" }).click();

    const country = page.getByLabel("Country");
    await expect(country).toBeEnabled();
    await expect.poll(() => country.locator("option").count()).toBeGreaterThan(1);
    const countryId = await country.locator('option:not([value=""])').first().getAttribute("value");
    if (!countryId) {
      throw new Error("The backend did not provide a selectable country.");
    }
    await country.selectOption(countryId);
    await page.getByLabel("Street address").fill("100 E2E Test Road");
    await page.getByLabel("Postal code").fill("560001");
    await page.getByRole("button", { name: "Review workspace →" }).click();

    await expect(page.getByText(organizationName, { exact: true })).toHaveCount(2);
    const signupResponsePromise = page.waitForResponse(
      (response) =>
        new URL(response.url()).pathname.endsWith("/api/onboarding/signup/") &&
        response.request().method() === "POST",
    );
    await page.getByRole("button", { name: /Create workspace/ }).click();

    const signupResponse = await signupResponsePromise;
    expect(signupResponse.status()).toBe(201);
    const signupEnvelope = (await signupResponse.json()) as {
      success: boolean;
      data: {
        signup: { status: string; verification_required: boolean };
        account: { email: string; email_verified: boolean };
        organization: { id: string; name: string; organization_type: string };
        subscription: { id: string };
        payment: { required_now: boolean };
      };
    };

    expect(signupEnvelope.success).toBe(true);
    expect(signupEnvelope.data.signup).toMatchObject({
      status: "PENDING_EMAIL_VERIFICATION",
      verification_required: true,
    });
    expect(signupEnvelope.data.account).toMatchObject({
      email,
      email_verified: false,
    });
    expect(signupEnvelope.data.organization).toMatchObject({
      id: expect.any(String),
      name: organizationName,
      organization_type: "retail_pharmacy",
    });
    expect(signupEnvelope.data.subscription.id).toBeTruthy();
    expect(signupEnvelope.data.payment.required_now).toBe(false);

    await expect(page).toHaveURL(/\/verify-email\?email=/);
    await expect(
      page.getByRole("heading", { name: "Verify your email" }),
    ).toBeVisible();
    await expect(page.getByLabel("Email")).toHaveValue(email);
  });

  test("billing page clearly reports checkout availability without a browser alert", async ({
    page,
  }) => {
    page.on("dialog", async (dialog) => {
      throw new Error(`Unexpected browser dialog: ${dialog.message()}`);
    });

    await page.goto("/billing?plan=Starter%20Clinic&amount=2623.25&currency=INR&cycle=monthly");
    await expect(
      page.getByRole("heading", { name: "Review your plan" }),
    ).toBeVisible();

    await expect(page.getByRole("heading", { name: "Starter Clinic" })).toBeVisible();
    await expect(page.getByText("₹2,623.25")).toHaveCount(2);
    await expect(
      page.getByRole("status").getByText("Online checkout is not available yet"),
    ).toBeVisible();
    await expect(
      page.getByRole("button", { name: "Checkout not available" }),
    ).toBeDisabled();
  });
});
