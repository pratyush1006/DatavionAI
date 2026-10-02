import { expect, test } from "@playwright/test";

const organization = "00000000-0000-4000-8000-000000000030";
const user = { id: "00000000-0000-4000-8000-000000000031", email: "technician@example.test", first_name: "Priya", last_name: "Rao", is_verified: true, is_active: true, is_platform_admin: true };
const envelope = (data: unknown) => ({ success: true, message: "Success", data, meta: {} });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(({ user }) => {
    for (const [key, value] of Object.entries({ access_token: "diagnostic-token", refresh_token: "diagnostic-refresh", current_user: user })) {
      const entry = JSON.stringify({ value, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
      localStorage.setItem(`datavion:v1:${key}`, entry);
      sessionStorage.setItem(`datavion:v1:${key}`, entry);
    }
  }, { user });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let data: unknown = { results: [], count: 0 };
    if (path.endsWith("/auth/me/")) data = user;
    else if (path.endsWith("/bootstrap/")) data = { user, tenant: { id: organization, name: "ABC Healthcare", tenant_type: "hospital", status: "ACTIVE" }, organization: { id: organization, name: "ABC Healthcare" }, employee: null, access_context: { organization_id: organization, department_ids: [], team_ids: [], subscription_active: true }, permissions: ["*"], organization_roles: ["laboratory_technician", "imaging_technician"], platform_roles: [], navigation: [], dashboard: [], branding: {}, feature_flags: {}, subscription: null, preferences: {}, modules: ["laboratory", "imaging"].map((identifier) => ({ identifier, name: identifier, display_name: identifier, description: identifier, version: "1.0.0", category: "clinical", route: `/workspace/${identifier}`, api_prefix: `/api/${identifier}`, icon: "activity", permissions: ["*"], enabled: true, system: false, tenant_scoped: true, order: 1, tags: [], feature_flags: [] })) };
    else if (path.endsWith("/laboratories/laboratories/")) data = { results: [{ id: "lab-1", code: "LAB", name: "Central Lab", status: "active" }] };
    else if (path.endsWith("/laboratories/orders/")) data = { results: [{ id: "lo-1", order_number: "LAB-1001", patient_name: "Patient A", status: "ordered", priority: "urgent", items: [] }] };
    else if (path.endsWith("/laboratories/results/")) data = { results: [{ id: "lr-1", status: "preliminary", value_text: "Critical potassium", abnormal_flag: "critical_high", critical: true }] };
    else if (path.endsWith("/laboratories/specimens/")) data = { results: [{ id: "sp-1", specimen_id: "SP-1001", order_number: "LAB-1001", specimen_type: "blood", status: "collected" }] };
    else if (path.endsWith("/imaging/orders/")) data = { results: [{ id: "io-1", order_number: "IMG-1001", patient_id: "patient-a", priority: "stat", status: "ordered", clinical_indication: "Head trauma" }] };
    else if (path.endsWith("/imaging/studies/")) data = { results: [{ id: "is-1", accession_number: "ACC-1001", procedure_name: "CT Head", modality_name: "CT", order_number: "IMG-1001", status: "scheduled" }] };
    await route.fulfill({ json: envelope(data) });
  });
});

test("lab technician sees worklist and advances a sample", async ({ page }) => {
  await page.goto("/workspace/laboratory", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Lab Technician/ })).toBeVisible();
  await expect(page.getByText("LAB-1001")).toBeVisible();
  await expect(page.getByText("Critical potassium")).toBeVisible();
  await page.goto("/workspace/laboratory?section=specimens", { waitUntil: "domcontentloaded" });
  const request = page.waitForRequest((item) => item.method() === "POST" && item.url().endsWith("/laboratories/specimens/sp-1/receive/"));
  await page.getByRole("button", { name: "Receive" }).click();
  await request;
});

test("imaging technician sees worklist and priority cases", async ({ page }) => {
  await page.goto("/workspace/imaging", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Imaging Technician/ })).toBeVisible();
  await expect(page.getByText("CT Head")).toBeVisible();
  await expect(page.getByText("Head trauma")).toBeVisible();
});
