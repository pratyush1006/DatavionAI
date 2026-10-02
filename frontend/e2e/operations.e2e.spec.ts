import { expect, test } from "@playwright/test";

const organization = "00000000-0000-4000-8000-000000000040";
const user = { id: "00000000-0000-4000-8000-000000000041", email: "manager@example.test", first_name: "Asha", last_name: "Rao", is_verified: true, is_active: true, is_platform_admin: true };
const envelope = (data: unknown) => ({ success: true, message: "Success", data, meta: {} });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(({ user }) => { for (const [key, value] of Object.entries({ access_token: "manager-token", refresh_token: "manager-refresh", current_user: user })) { const entry = JSON.stringify({ value, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() }); localStorage.setItem(`datavion:v1:${key}`, entry); sessionStorage.setItem(`datavion:v1:${key}`, entry); } }, { user });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname; let data: unknown = { results: [], count: 0 };
    if (path.endsWith("/auth/me/")) data = user;
    else if (path.endsWith("/bootstrap/")) data = { user, tenant: { id: organization, name: "ABC Healthcare", tenant_type: "hospital", status: "ACTIVE" }, organization: { id: organization, name: "ABC Healthcare" }, employee: null, access_context: { organization_id: organization, department_ids: [], team_ids: [], subscription_active: true }, permissions: ["*"], organization_roles: ["inventory_manager", "department_manager"], platform_roles: [], navigation: [], dashboard: [], branding: {}, feature_flags: {}, subscription: null, preferences: {}, modules: ["inventory", "department-manager"].map((identifier) => ({ identifier, name: identifier, display_name: identifier, description: identifier, version: "1.0.0", category: "operations", route: `/workspace/${identifier}`, api_prefix: `/api/${identifier}`, icon: "activity", permissions: ["*"], enabled: true, system: false, tenant_scoped: true, order: 1, tags: [], feature_flags: [] })) };
    else if (path.endsWith("/pharmacy/pharmacies/")) data = { results: [{ id: "warehouse-1", code: "CENTRAL", name: "Central Inventory", status: "active" }] };
    else if (path.endsWith("/pharmacy/products/")) data = { results: [{ id: "product-1", sku: "SKU-100" }] };
    else if (path.endsWith("/pharmacy/batches/")) data = { results: [{ id: "batch-1", batch_number: "B-100", expiry_date: "2026-10-20" }] };
    else if (path.endsWith("/pharmacy/inventory/")) data = [{ product_id: "product-1", sku: "SKU-100", medication: "Item A", stock: "0", reorder_level: "10" }];
    else if (path.endsWith("/pharmacy/stock-movements/")) data = { results: [{ id: "move-1", sku: "SKU-100", medication_name: "Item A", batch_number: "B-100", movement_type: "receipt", quantity: "20" }] };
    else if (path.endsWith("/pharmacy/stock-transfers/")) data = { results: [{ id: "transfer-1", transfer_number: "TR-100", source_name: "Central", destination_name: "Ward", status: "approved" }] };
    else if (path.endsWith("/departments/")) data = { results: [{ id: "dept-1", code: "CARD", name: "Cardiology", status: "active" }] };
    else if (path.endsWith("/employees/")) data = { results: [{ id: "staff-1", employee_code: "EMP-1", full_name: "Dr A", department_id: "dept-1", is_active: true }] };
    else if (path.endsWith("/patients/")) data = { results: [{ id: "patient-1", patient_number: "P-1", display_name: "Patient A", status: "active" }] };
    else if (path.endsWith("/nursing/tasks/")) data = { results: [{ id: "task-1", title: "Review patient", department_id: "dept-1", priority: "high", status: "pending" }] };
    await route.fulfill({ json: envelope(data) });
  });
});

test("inventory manager sees alerts and completes a transfer", async ({ page }) => {
  await page.goto("/workspace/inventory", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Inventory Manager/ })).toBeVisible(); await expect(page.getByText("1 out of stock")).toBeVisible();
  await page.goto("/workspace/inventory?section=transfers", { waitUntil: "domcontentloaded" }); const request = page.waitForRequest((item) => item.method() === "POST" && item.url().endsWith("/pharmacy/stock-transfers/transfer-1/complete/")); await page.getByRole("button", { name: "Complete" }).click(); await request;
});

test("department manager sees KPIs and completes a task", async ({ page }) => {
  await page.goto("/workspace/department-manager", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Department Manager/ })).toBeVisible(); await expect(page.getByText("Cardiology")).toBeVisible();
  await page.goto("/workspace/department-manager?section=tasks", { waitUntil: "domcontentloaded" }); const request = page.waitForRequest((item) => item.method() === "POST" && item.url().endsWith("/nursing/tasks/task-1/complete/")); await page.getByRole("button", { name: "Complete" }).click(); await request;
});
