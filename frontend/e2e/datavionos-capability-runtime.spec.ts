import {
  expect,
  test,
  type APIRequestContext,
} from "@playwright/test";

function getRequiredEnvironmentValue(
  key: string,
): string {
  const value =
    process.env[key]?.trim();

  if (!value) {
    throw new Error(
      `DatavionOS E2E configuration error: ${key} is not configured.`,
    );
  }

  return value;
}

const API_BASE_URL =
  getRequiredEnvironmentValue(
    "NEXT_PUBLIC_API_BASE_URL",
  ).replace(
    /\/+$/,
    "",
  );

const DASHBOARD_URL =
  process.env.DATAVIONOS_DASHBOARD_URL ??
  "http://localhost:3000/dashboard";

type EffectiveCapabilityResponse = {
  success: boolean;
  user_id?: string;
  organization_id?: string;
  tenant_id?: string;
  modules?: Record<string, unknown>;
  module_state?: Record<string, unknown>;
  features?: Record<string, unknown>;
  permissions?: string[];
  roles?: string[];
  departments?: string[];
  ai_capabilities?: Record<string, unknown>;
  limits?: Record<string, unknown>;
  effective_capabilities?:
    Record<string, unknown>;
};

async function readEffectiveCapability(
  request: APIRequestContext,
): Promise<EffectiveCapabilityResponse> {
  const response =
    await request.get(
      `${API_BASE_URL}/datavionos/effective-context/`,
    );

  expect(
    response.ok(),
  ).toBeTruthy();

  return response.json();
}

function isEnabled(
  value: unknown,
): boolean {
  if (
    typeof value ===
    "boolean"
  ) {
    return value;
  }

  if (
    typeof value ===
      "object" &&
    value !== null &&
    "enabled" in value
  ) {
    return Boolean(
      (
        value as {
          enabled?: unknown;
        }
      ).enabled,
    );
  }

  return Boolean(value);
}

test.describe(
  "DatavionOS Dynamic Dashboard Runtime",
  () => {
    test(
      "effective capability API is the dashboard authority",
      async ({
        request,
      }) => {
        const context =
          await readEffectiveCapability(
            request,
          );

        expect(
          context.success,
        ).toBeTruthy();

        expect(
          context.organization_id,
        ).toBeTruthy();

        expect(
          context.modules ??
            context.module_state,
        ).toBeDefined();

        expect(
          context.features,
        ).toBeDefined();

        expect(
          context.permissions,
        ).toBeDefined();

        expect(
          context.ai_capabilities,
        ).toBeDefined();

        expect(
          context.effective_capabilities,
        ).toBeDefined();
      },
    );

    test(
      "dashboard loads from effective capability runtime",
      async ({
        page,
      }) => {
        await page.goto(
          DASHBOARD_URL,
        );

        await expect(
          page.locator(
            "[data-datavionos-dashboard]",
          ),
        ).toBeVisible();
      },
    );

    test(
      "disabled modules are not exposed",
      async ({
        page,
        request,
      }) => {
        const context =
          await readEffectiveCapability(
            request,
          );

        await page.goto(
          DASHBOARD_URL,
        );

        const modules =
          context.modules ??
          context.module_state ??
          {};

        for (
          const [
            moduleCode,
            moduleState,
          ] of Object.entries(
            modules,
          )
        ) {
          const selector =
            `[data-module-code="${moduleCode}"]`;

          const item =
            page.locator(
              selector,
            );

          if (
            await item.count()
          ) {
            if (
              !isEnabled(
                moduleState,
              )
            ) {
              await expect(
                item,
              ).toHaveCount(0);
            }
          }
        }
      },
    );

    test(
      "dynamic navigation is visible",
      async ({
        page,
      }) => {
        await page.goto(
          DASHBOARD_URL,
        );

        await expect(
          page.locator(
            "[data-datavionos-navigation]",
          ),
        ).toBeVisible();
      },
    );

    test(
      "AI capability state follows effective authority",
      async ({
        request,
        page,
      }) => {
        const context =
          await readEffectiveCapability(
            request,
          );

        await page.goto(
          DASHBOARD_URL,
        );

        const capabilities =
          context.ai_capabilities ??
          {};

        for (
          const [
            code,
            state,
          ] of Object.entries(
            capabilities,
          )
        ) {
          const selector =
            `[data-ai-capability-code="${code}"]`;

          const item =
            page.locator(
              selector,
            );

          if (
            await item.count()
          ) {
            if (
              !isEnabled(state)
            ) {
              await expect(
                item,
              ).toHaveCount(0);
            }
          }
        }
      },
    );

    test(
      "RBAC remains part of effective capability authority",
      async ({
        request,
      }) => {
        const context =
          await readEffectiveCapability(
            request,
          );

        expect(
          Array.isArray(
            context.permissions,
          ),
        ).toBeTruthy();

        expect(
          context.effective_capabilities,
        ).toBeDefined();
      },
    );
  },
);
