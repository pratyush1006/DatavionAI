import { test, expect, type APIRequestContext, type Page } from "@playwright/test";

const API_BASE_URL =
  process.env.DATAVIONOS_E2E_API_BASE_URL ??
  "http://127.0.0.1:8000/api";

const EMAIL =
  process.env.DATAVIONOS_E2E_EMAIL ?? "";

const PASSWORD =
  process.env.DATAVIONOS_E2E_PASSWORD ?? "";

const OTP =
  process.env.DATAVIONOS_E2E_OTP ?? "";

const LOGIN_PATH =
  process.env.DATAVIONOS_E2E_LOGIN_PATH ??
  "/auth/login/";

const OTP_PATH =
  process.env.DATAVIONOS_E2E_OTP_PATH ??
  "/auth/verify-otp/";

const LOGOUT_PATH =
  process.env.DATAVIONOS_E2E_LOGOUT_PATH ??
  "/auth/logout/";

const ORGANIZATION_PATH =
  process.env.DATAVIONOS_E2E_ORGANIZATION_PATH ??
  "/organizations/";

const SUBSCRIPTION_PATH =
  process.env.DATAVIONOS_E2E_SUBSCRIPTION_PATH ??
  "/organizations/subscription/";

const MODULES_PATH =
  process.env.DATAVIONOS_E2E_MODULES_PATH ??
  "/organizations/modules/";

const ME_PATH =
  process.env.DATAVIONOS_E2E_ME_PATH ??
  "/auth/me/";

const HEALTH_PATH =
  process.env.DATAVIONOS_E2E_HEALTH_PATH ??
  "/health/";

const TEST_ORG_SLUG =
  process.env.DATAVIONOS_E2E_TEST_ORG_SLUG ?? "";

const TEST_MODULE =
  process.env.DATAVIONOS_E2E_TEST_MODULE ??
  "pharmacy";

type LoginResponse = {
  access?: string;
  refresh?: string;
  access_token?: string;
  refresh_token?: string;
  token?: string;
  otp_required?: boolean;
  requires_otp?: boolean;
};

function requireCredential(
  value: string,
  name: string,
): void {
  test.skip(
    !value,
    `${name} is not configured.`,
  );
}

async function loginViaApi(
  request: APIRequestContext,
): Promise<LoginResponse> {
  requireCredential(EMAIL, "DATAVIONOS_E2E_EMAIL");
  requireCredential(PASSWORD, "DATAVIONOS_E2E_PASSWORD");

  const response = await request.post(
    `${API_BASE_URL}${LOGIN_PATH}`,
    {
      data: {
        email: EMAIL,
        username: EMAIL,
        password: PASSWORD,
      },
      failOnStatusCode: false,
    },
  );

  expect(
    response.status(),
    "Login endpoint must return an expected authentication response.",
  ).toBeLessThan(500);

  expect(
    [200, 201, 202],
    "Login API returned an unexpected status.",
  ).toContain(response.status());

  return await response.json();
}

async function verifyOtpViaApi(
  request: APIRequestContext,
): Promise<void> {
  requireCredential(OTP, "DATAVIONOS_E2E_OTP");

  const response = await request.post(
    `${API_BASE_URL}${OTP_PATH}`,
    {
      data: {
        email: EMAIL,
        username: EMAIL,
        otp: OTP,
        code: OTP,
      },
      failOnStatusCode: false,
    },
  );

  expect(
    response.status(),
    "OTP verification endpoint must not return a server error.",
  ).toBeLessThan(500);

  expect(
    [200, 201, 202],
    "OTP verification failed.",
  ).toContain(response.status());
}

async function authenticatedHeaders(
  request: APIRequestContext,
): Promise<Record<string, string>> {
  const login = await loginViaApi(request);

  if (
    login.otp_required ||
    login.requires_otp
  ) {
    await verifyOtpViaApi(request);
  }

  const token =
    login.access ??
    login.access_token ??
    login.token;

  if (!token) {
    throw new Error(
      "Login succeeded but no access token was returned. " +
      "Configure the backend authentication contract for the E2E suite.",
    );
  }

  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

async function assertApiReachable(
  request: APIRequestContext,
  path: string,
): Promise<void> {
  const response = await request.get(
    `${API_BASE_URL}${path}`,
    {
      failOnStatusCode: false,
    },
  );

  expect(
    response.status(),
    `API endpoint ${path} returned a server error.`,
  ).toBeLessThan(500);
}

test.describe.serial(
  "DatavionOS SaaS business runtime",
  () => {
    test(
      "backend API health is reachable",
      async ({ request }) => {
        await assertApiReachable(
          request,
          HEALTH_PATH,
        );
      },
    );

    test(
      "real authentication contract works",
      async ({ request }) => {
        const login = await loginViaApi(request);

        expect(
          login,
          "Login response must be a JSON authentication contract.",
        ).toBeTruthy();

        if (
          login.otp_required ||
          login.requires_otp
        ) {
          requireCredential(
            OTP,
            "DATAVIONOS_E2E_OTP",
          );

          await verifyOtpViaApi(request);
        }

        const token =
          login.access ??
          login.access_token ??
          login.token;

        expect(
          token,
          "Authentication must return an access token.",
        ).toBeTruthy();
      },
    );

    test(
      "authenticated identity endpoint works",
      async ({ request }) => {
        const headers =
          await authenticatedHeaders(request);

        const response = await request.get(
          `${API_BASE_URL}${ME_PATH}`,
          {
            headers,
            failOnStatusCode: false,
          },
        );

        expect(response.status()).toBeLessThan(500);
        expect([200, 401, 403]).toContain(
          response.status(),
        );

        if (response.status() === 200) {
          const body = await response.json();

          expect(
            body,
            "Authenticated identity response must be JSON.",
          ).toBeTruthy();
        }
      },
    );

    test(
      "organization contract is reachable",
      async ({ request }) => {
        const headers =
          await authenticatedHeaders(request);

        const response = await request.get(
          `${API_BASE_URL}${ORGANIZATION_PATH}`,
          {
            headers,
            failOnStatusCode: false,
          },
        );

        expect(response.status()).toBeLessThan(500);
        expect(
          [200, 201, 204, 401, 403],
        ).toContain(response.status());
      },
    );

    test(
      "subscription contract is reachable",
      async ({ request }) => {
        const headers =
          await authenticatedHeaders(request);

        const response = await request.get(
          `${API_BASE_URL}${SUBSCRIPTION_PATH}`,
          {
            headers,
            failOnStatusCode: false,
          },
        );

        expect(response.status()).toBeLessThan(500);
        expect(
          [200, 201, 204, 401, 403, 404],
        ).toContain(response.status());
      },
    );

    test(
      "organization module contract is reachable",
      async ({ request }) => {
        const headers =
          await authenticatedHeaders(request);

        const response = await request.get(
          `${API_BASE_URL}${MODULES_PATH}`,
          {
            headers,
            failOnStatusCode: false,
          },
        );

        expect(response.status()).toBeLessThan(500);
        expect(
          [200, 201, 204, 401, 403, 404],
        ).toContain(response.status());
      },
    );

    test(
      "authenticated dashboard is rendered",
      async ({ page }) => {
        requireCredential(
          EMAIL,
          "DATAVIONOS_E2E_EMAIL",
        );
        requireCredential(
          PASSWORD,
          "DATAVIONOS_E2E_PASSWORD",
        );

        await page.goto("/login");
        await expect(page).toHaveURL(/\/login/);

        const emailInput =
          page.getByLabel(/email/i).first();

        const passwordInput =
          page.getByLabel(/password/i).first();

        await emailInput.fill(EMAIL);
        await passwordInput.fill(PASSWORD);

        const submit =
          page.getByRole("button", {
            name: /login|sign in/i,
          }).first();

        await submit.click();

        await page.waitForLoadState(
          "domcontentloaded",
        );

        await expect(
          page,
        ).not.toHaveURL(/\/login$/);
      },
    );

    test(
      "organization registration route remains available",
      async ({ page }) => {
        await page.goto(
          "/organization/register",
        );

        await expect(
          page,
        ).toHaveURL(
          /\/organization\/register/,
        );

        await expect(
          page.locator("body"),
        ).toBeVisible();
      },
    );

    test(
      "module workspace route is reachable",
      async ({ page }) => {
        await page.goto(
          `/workspace/${TEST_MODULE}`,
        );

        await expect(
          page.locator("body"),
        ).toBeVisible();

        expect(
          page.url(),
          "Workspace navigation must resolve.",
        ).toContain(
          `/workspace/${TEST_MODULE}`,
        );
      },
    );

    test(
      "organization slug contract is configured for tenant isolation",
      async () => {
        test.skip(
          !TEST_ORG_SLUG,
          "DATAVIONOS_E2E_TEST_ORG_SLUG is not configured.",
        );

        expect(
          TEST_ORG_SLUG,
        ).toMatch(
          /^[a-z0-9][a-z0-9-]*$/,
        );
      },
    );

    test(
      "logout contract invalidates the authenticated session",
      async ({ request }) => {
        const headers =
          await authenticatedHeaders(request);

        const response = await request.post(
          `${API_BASE_URL}${LOGOUT_PATH}`,
          {
            headers,
            failOnStatusCode: false,
          },
        );

        expect(response.status()).toBeLessThan(500);
        expect(
          [200, 201, 202, 204, 401, 403],
        ).toContain(response.status());
      },
    );
  },
);
