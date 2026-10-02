import { test, expect } from "@playwright/test";

const organization = "00000000-0000-4000-8000-000000000001";
const employee = "00000000-0000-4000-8000-000000000002";
const user = { id: employee, email: "hr@test.com", first_name: "HR", last_name: "Admin", is_verified: true, is_active: true, is_platform_admin: true };
const envelope = (data: unknown, meta: unknown = {}) => ({ success: true, message: "Success", data, meta });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(({ user }) => {
    for (const [key, value] of Object.entries({ access_token: "hr-test-token", refresh_token: "hr-test-refresh", current_user: user })) {
      const entry = JSON.stringify({ value, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
      localStorage.setItem(`datavion:v1:${key}`, entry);
      sessionStorage.setItem(`datavion:v1:${key}`, entry);
    }
  }, { user });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let data: unknown = [];
    if (path.endsWith("/auth/me/")) data = user;
    else if (path.endsWith("/bootstrap/")) data = {
      user, tenant: { id: organization, name: "HR Hospital", tenant_type: "hospital", status: "ACTIVE" },
      organization: { id: organization, name: "HR Hospital" }, employee: null,
      access_context: { organization_id: organization, department_id: null, team_id: null },
      permissions: ["*"], platform_roles: [], organization_roles: [], navigation: [], dashboard: [], branding: {}, feature_flags: {}, subscription: null, preferences: {},
      modules: [{ identifier: "hr", display_name: "Human Resources", name: "Human Resources", category: "utility", route: "/workspace/hr", api_prefix: "/api/hr", version: "1.0.0", permissions: ["hr.view"], tenant_scoped: true, tags: [] }],
    };
    else if (path.endsWith("/employees/")) data = [{ id: employee, full_name: "Test Employee", employee_code: "EMP001" }];
    else if (path.endsWith("/hr/leave/types/")) data = [{ id: 1, name: "Annual leave" }];
    await route.fulfill({ json: envelope(data, { pagination: { count: Array.isArray(data) ? data.length : 0, next: null } }) });
  });
});

test("HR renders operational sections and submits attendance with time values", async ({ page }) => {
  await page.goto("/workspace/hr?section=attendance");
  await expect(page.getByRole("heading", { name: "Human Resources" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Performance goals", exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: "Open module" })).toHaveCount(0);
  await page.getByRole("button", { name: "Create record" }).click();
  await page.getByLabel("Employee *", { exact: true }).selectOption(employee);
  await page.getByLabel("Work date *").fill("2026-10-01");
  await page.getByLabel("Check in", { exact: true }).fill("09:00");
  await page.getByLabel("Check out", { exact: true }).fill("17:00");
  const submitted = page.waitForRequest((request) => request.method() === "POST" && request.url().includes("/hr/attendance/"));
  await page.getByRole("button", { name: "Save record" }).click();
  const request = await submitted;
  expect(request.postDataJSON()).toMatchObject({ organization, employee, check_in: "09:00", check_out: "17:00", work_date: "2026-10-01" });
  await expect(page.getByText("Record saved.")).toBeVisible();
});

test("leave approval sends decision notes and refreshes the list", async ({ page }) => {
  let status = "pending";
  await page.route("**/api/hr/leave/requests/**", async (route) => {
    if (route.request().method() === "POST") {
      expect(route.request().url()).toContain("/1/approve/");
      expect(route.request().postDataJSON()).toEqual({ decision_notes: "Approved by HR" });
      status = "approved";
      await route.fulfill({ json: envelope({ status }) });
    } else await route.fulfill({ json: envelope([{ id: 1, employee_name: "Test Employee", leave_type: "Annual", start_date: "2026-10-02", end_date: "2026-10-03", number_of_days: "2", status }]) });
  });
  await page.goto("/workspace/hr?section=requests");
  await page.getByRole("button", { name: "Leave requests", exact: true }).click();
  await page.getByRole("button", { name: "Approve", exact: true }).click();
  await page.getByLabel("Decision notes").fill("Approved by HR");
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect(page.getByText("Approve completed.")).toBeVisible();
  await expect(page.getByRole("cell", { name: "Approved", exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Approve", exact: true })).toHaveCount(0);
});

test("leave creation loads employee and leave type relationships", async ({ page }) => {
  await page.goto("/workspace/hr?section=requests");
  await page.getByRole("button", { name: "Create record" }).click();
  await page.getByLabel("Employee *", { exact: true }).selectOption(employee);
  await page.getByLabel("Leave type *").selectOption("1");
  await page.getByLabel("Start date *").fill("2026-10-02");
  await page.getByLabel("End date *").fill("2026-10-02");
  await page.getByLabel("Number of days *").fill("1");
  const submitted = page.waitForRequest((request) => request.method() === "POST" && request.url().includes("/hr/leave/requests/"));
  await page.getByRole("button", { name: "Save record" }).click();
  expect((await submitted).postDataJSON()).toMatchObject({ organization, employee, leave_type: "1", number_of_days: 1 });
  await expect(page.getByText("Record saved.")).toBeVisible();
});

test("editing preserves employee UUID and payroll components", async ({ page }) => {
  await page.route("**/api/hr/payroll/payslips/**", async (route) => {
    if (route.request().method() === "PATCH") {
      expect(route.request().postDataJSON()).toMatchObject({ employee, basic_salary: 1200, line_items: [{ component_type: "deduction", name: "Tax", amount: "50" }] });
      await route.fulfill({ json: envelope({ id: 1 }) });
    } else if (new URL(route.request().url()).pathname.endsWith("/1/")) {
      await route.fulfill({ json: envelope({ id: 1, employee: "EMP001", employee_id: employee, pay_period_start: "2026-10-01", pay_period_end: "2026-10-31", basic_salary: "1000", total_allowances: "100", currency: "INR", notes: "", line_items: [{ id: 10, component_type: "deduction", name: "Tax", amount: "50" }] }) });
    } else await route.fulfill({ json: envelope([{ id: 1, employee_name: "Test Employee", status: "draft" }]) });
  });
  await page.goto("/workspace/hr?section=payslips");
  await page.getByRole("button", { name: "Payslips", exact: true }).click();
  await page.getByRole("button", { name: "Edit", exact: true }).click();
  await expect(page.getByLabel("Employee *", { exact: true })).toHaveValue(employee);
  await page.getByLabel("Basic salary *").fill("1200");
  await page.getByRole("button", { name: "Save record" }).click();
  await expect(page.getByText("Record saved.")).toBeVisible();
});

test("executive overview uses live metrics and navigates employee search and HR actions", async ({ page }) => {
  const today = new Date().toLocaleDateString("en-CA");
  await page.route("**/api/employees/**", (route) => route.fulfill({ json: envelope([
    { id: employee, full_name: "Test Employee", employee_code: "EMP001", joining_date: today, status: "ACTIVE", designation: "Nurse" },
    { id: "employee-2", full_name: "Other Employee", employee_code: "EMP002", joining_date: "2025-01-01", status: "ACTIVE", designation: "Doctor" },
  ]) }));
  await page.route("**/api/hr/attendance/**", (route) => route.fulfill({ json: envelope([{ id: 1, employee: "EMP001", employee_name: "Test Employee", work_date: today, status: "present" }]) }));
  await page.route("**/api/hr/leave/requests/**", (route) => route.fulfill({ json: envelope([
    { id: 1, employee: "EMP002", status: "approved", start_date: today, end_date: today },
    { id: 2, employee: "EMP001", employee_name: "Test Employee", status: "pending", start_date: today, end_date: today },
  ]) }));
  await page.goto("/workspace/hr");
  await expect(page.getByRole("heading", { name: /HR Executive/ })).toBeVisible();
  await expect(page.getByTestId("hr-metric-employees")).toHaveText("2");
  await expect(page.getByTestId("hr-metric-present")).toHaveText("1");
  await expect(page.getByTestId("hr-metric-on-leave")).toHaveText("1");
  await expect(page.getByTestId("hr-metric-approvals")).toHaveText("1");
  await expect(page.getByRole("img", { name: /Headcount chart/ })).toBeVisible();
  await page.screenshot({ path: "test-results/hr-executive-dashboard.png", fullPage: true });
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export", exact: true }).click();
  expect((await download).suggestedFilename()).toContain("hr-headcount-");
  await page.getByLabel("Search employees", { exact: true }).fill("Test Employee");
  await page.getByLabel("Search employees", { exact: true }).press("Enter");
  await expect(page).toHaveURL(/section=employees&search=Test%20Employee/);
  await expect(page.getByRole("table")).toContainText("Test Employee");
  await expect(page.getByRole("table")).not.toContainText("Other Employee");
  await page.getByRole("navigation", { name: "HR navigation" }).getByRole("link", { name: "Leave", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Leave requests", exact: true })).toBeVisible();
});

test("dashboard distinguishes failed metrics from zero and exposes recruitment availability", async ({ page }) => {
  await page.route("**/api/hr/attendance/**", (route) => route.fulfill({ status: 500, json: { success: false, error: { code: "INTERNAL_SERVER_ERROR", message: "Attendance unavailable", details: null } } }));
  await page.goto("/workspace/hr");
  await expect(page.getByRole("alert").filter({ hasText: "Could not load attendance" })).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId("hr-metric-present")).toHaveText("—");
  await page.getByRole("navigation", { name: "HR navigation" }).getByRole("link", { name: "Recruitment", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Job openings", exact: true })).toBeVisible();
});

test("manager dashboard shows workforce analytics and retains manager navigation", async ({ page }) => {
  const today = new Date().toLocaleDateString("en-CA");
  await page.route("**/api/employees/**", (route) => route.fulfill({ json: envelope([
    { id: employee, employee_code: "EMP001", full_name: "Test Employee", employment_type: "FULL_TIME", joining_date: "2025-01-01", status: "ACTIVE" },
    { id: "departed", employee_code: "EMP002", full_name: "Former Employee", joining_date: "2025-01-01", termination_date: today, status: "TERMINATED" },
  ]) }));
  await page.route("**/api/hr/attendance/**", (route) => route.fulfill({ json: envelope([{ id: 1, employee: "EMP001", work_date: today, status: "present" }]) }));
  await page.route("**/api/departments/**", (route) => route.fulfill({ json: envelope([{ id: "cardiology", name: "Cardiology", code: "CARD" }]) }));
  await page.goto("/workspace/hr?view=manager");
  await expect(page.getByRole("heading", { name: /HR Manager/ })).toBeVisible();
  await expect(page.getByTestId("hr-metric-headcount")).toHaveText("1");
  await expect(page.getByTestId("hr-metric-attendance")).toHaveText("100%");
  await expect(page.getByTestId("hr-metric-turnover")).toHaveText("66.7%");
  await expect(page.getByTestId("hr-metric-open-jobs")).toHaveText("0");
  await expect(page.getByRole("heading", { name: "Manager Actions" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Employee Distribution" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Leave Trends" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Recent Activity" })).toBeVisible();
  await page.screenshot({ path: "test-results/hr-manager-dashboard.png", fullPage: true });
  await page.getByLabel("Search employees", { exact: true }).fill("Cardiology");
  await page.getByLabel("Search employees", { exact: true }).press("Enter");
  await expect(page).toHaveURL(/view=manager/);
  await expect(page.getByRole("link", { name: "Cardiology · CARD" })).toBeVisible();
  await page.getByRole("navigation", { name: "HR navigation" }).getByRole("link", { name: "HR Analytics" }).click();
  await expect(page).toHaveURL(/section=reports&view=manager/);
  await page.getByLabel("Dashboard view", { exact: true }).selectOption("executive");
  await expect(page.getByRole("heading", { name: /HR Executive/ })).toBeVisible();
});
