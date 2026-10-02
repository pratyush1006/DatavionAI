import { expect, test } from "@playwright/test";

const organization = "00000000-0000-4000-8000-000000000020";
const pharmacy = "00000000-0000-4000-8000-000000000021";
const user = { id: "00000000-0000-4000-8000-000000000022", email: "pharmacist@example.test", first_name: "Asha", last_name: "Shah", is_verified: true, is_active: true, is_platform_admin: true };
const envelope = (data: unknown) => ({ success: true, message: "Success", data, meta: {} });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(({ user }) => {
    for (const [key, value] of Object.entries({ access_token: "pharmacy-token", refresh_token: "pharmacy-refresh", current_user: user })) {
      const entry = JSON.stringify({ value, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
      localStorage.setItem(`datavion:v1:${key}`, entry);
      sessionStorage.setItem(`datavion:v1:${key}`, entry);
    }
  }, { user });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let data: unknown = { results: [], count: 0 };
    if (path.endsWith("/auth/me/")) data = user;
    else if (path.endsWith("/bootstrap/")) data = { user, tenant: { id: organization, name: "ABC Healthcare", tenant_type: "hospital", status: "ACTIVE" }, organization: { id: organization, name: "ABC Healthcare" }, employee: null, access_context: { organization_id: organization, department_ids: [], team_ids: [], subscription_active: true }, permissions: ["*"], organization_roles: ["pharmacist"], platform_roles: [], navigation: [], dashboard: [], branding: {}, feature_flags: {}, subscription: null, preferences: {}, modules: [{ identifier: "pharmacy", name: "Pharmacy", display_name: "Pharmacy", description: "Pharmacy", version: "1.0.0", category: "clinical", route: "/workspace/pharmacy", api_prefix: "/api/pharmacy", icon: "pill", permissions: ["pharmacy.view"], enabled: true, system: false, tenant_scoped: true, order: 1, tags: [], feature_flags: [] }] };
    else if (path.endsWith("/pharmacy/pharmacies/")) data = { results: [{ id: pharmacy, code: "PH01", name: "Main Pharmacy", status: "active" }], count: 1 };
    else if (path.endsWith("/pharmacy/dispensing-orders/")) data = { results: [{ id: "order-1", dispense_number: "D-100", prescription_number: "RX-10231", patient_name: "Patient A", pharmacy_name: "Main Pharmacy", status: "pending", lines: [] }], count: 1 };
    else if (path.endsWith("/pharmacy/summary/")) data = { low_stock_count: 1, expiring_batch_count: 1, low_stock: [{ id: "p1", sku: "MED-X" }], expiring_batches: [{ id: "b1", batch_number: "B-10", expiry_date: "2026-10-20" }] };
    else if (path.endsWith("/pharmacy/inventory/")) data = [{ product_id: "p1", sku: "MED-X", medication: "Medicine X", stock: "2", reorder_level: "10" }];
    await route.fulfill({ json: envelope(data) });
  });
});

test("pharmacist dashboard shows queue and inventory alerts", async ({ page }) => {
  await page.goto("/workspace/pharmacy", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Pharmacist/ })).toBeVisible();
  await expect(page.getByText("RX-10231")).toBeVisible();
  await expect(page.getByText("Patient A")).toBeVisible();
  await expect(page.getByText("MED-X low stock")).toBeVisible();
  await expect(page.getByText(/Batch B-10 expires/)).toBeVisible();
});

test("pharmacist can create a supplier", async ({ page }) => {
  await page.goto("/workspace/pharmacy?section=suppliers", { waitUntil: "domcontentloaded" });
  await page.getByRole("button", { name: "Create" }).click();
  await page.getByLabel("code *").fill("SUP-1");
  await page.getByLabel("name *", { exact: true }).fill("Reliable Supplier");
  await page.getByLabel("contact name *").fill("Ravi");
  await page.getByLabel("phone *").fill("9999999999");
  await page.getByLabel("email *").fill("supplier@example.test");
  await page.getByLabel("tax id *").fill("GST-100");
  await page.getByLabel("address *").fill("Mumbai");
  const request = page.waitForRequest((item) => item.method() === "POST" && item.url().endsWith("/pharmacy/suppliers/"));
  await page.getByRole("button", { name: "Save record" }).click();
  expect((await request).postDataJSON()).toMatchObject({ organization_id: organization, code: "SUP-1", name: "Reliable Supplier" });
});
