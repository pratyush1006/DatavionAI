"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  FileText,
  RefreshCw,
  Search,
  Wallet,
} from "lucide-react";

import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";

type CurrencyTotal = {
  currency: string;
  revenue_mtd: string;
  revenue_previous_month: string;
  revenue_change_percent: number | null;
  collected_mtd: string;
  collection_rate_percent: number | null;
  outstanding: string;
  overdue_amount: string;
  overdue_invoice_count: number;
};

type FinanceDashboardData = {
  as_of: string;
  period_start: string;
  period_end: string;
  currency_totals: CurrencyTotal[];
  trend: Array<{ month: string; currency: string; amount: string }>;
  recent_invoices: Array<{
    invoice_number: string;
    payer_name: string;
    claim_reference: string;
    currency: string;
    status: string;
    total: string;
    balance_due: string;
    due_date: string | null;
  }>;
  alerts: { overdue_invoice_count: number; open_denial_count: number };
};

const navigation = [
  { label: "Overview", href: "/workspace/revenue_cycle", icon: BarChart3 },
  { label: "Revenue", href: "#revenue", icon: Wallet },
  { label: "Invoices", href: "/workspace/billing", icon: FileText },
  { label: "Payments", href: "/workspace/payment_posting", icon: Wallet },
  { label: "Claims", href: "/workspace/claims", icon: FileText },
  { label: "RCM", href: "/workspace/revenue_cycle", icon: RefreshCw },
  { label: "Analytics", href: "/workspace/revenue_analytics", icon: BarChart3 },
  { label: "Reports", href: "/workspace/revenue_analytics", icon: FileText },
  { label: "Settings", href: "/organization/settings", icon: RefreshCw },
] as const;

const palette = ["#0d6efd", "#198754", "#fd7e14", "#6f42c1", "#dc3545"];

function amount(value: string, currency: string): string {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return "—";
  try {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(numeric);
  } catch {
    return `${currency} ${numeric.toLocaleString()}`;
  }
}

function monthLabels(asOf: string): string[] {
  const date = new Date(`${asOf}T00:00:00`);
  return Array.from({ length: 6 }, (_, index) => {
    const month = new Date(date.getFullYear(), date.getMonth() - 5 + index, 1);
    return `${month.getFullYear()}-${String(month.getMonth() + 1).padStart(2, "0")}-01`;
  });
}

function MetricCard({
  title,
  icon: Icon,
  rows,
  valueKey,
  detail,
}: {
  title: string;
  icon: typeof Wallet;
  rows: CurrencyTotal[];
  valueKey: "revenue_mtd" | "collected_mtd" | "outstanding" | "overdue_amount";
  detail: (row: CurrencyTotal) => string;
}) {
  return (
    <article className="card border-0 shadow-sm h-100">
      <div className="card-body p-3 p-lg-4">
        <div className="d-flex justify-content-between align-items-start gap-2 mb-3">
          <span className="small fw-medium text-body-secondary">{title}</span>
          <span className="rounded-3 bg-primary-subtle text-primary p-2"><Icon size={19} aria-hidden="true" /></span>
        </div>
        {rows.length ? rows.map((row) => (
          <div key={row.currency} className="mb-2 last-child-mb-0">
            <div className="h4 fw-semibold mb-0">{amount(row[valueKey], row.currency)}</div>
            <div className="small text-body-secondary">{row.currency} · {detail(row)}</div>
          </div>
        )) : <div className="h4 fw-semibold mb-0">—</div>}
      </div>
    </article>
  );
}

function RevenueTrend({ data, currency }: { data: FinanceDashboardData; currency: string }) {
  const labels = useMemo(() => monthLabels(data.as_of), [data.as_of]);
  const values = labels.map((month) => Number(data.trend.find((point) => point.currency === currency && point.month === month)?.amount ?? 0));
  const max = Math.max(1, ...values);

  if (!data.currency_totals.some((total) => total.currency === currency)) {
    return <div className="d-flex align-items-center justify-content-center text-body-secondary bg-body-tertiary rounded-3" style={{ minHeight: 230 }}>No finalized invoices in the last six months.</div>;
  }

  const coordinates = values.map((value, index) => `${52 + index * 112},${208 - value / max * 160}`).join(" ");
  return (
    <div>
      <svg className="w-100" viewBox="0 0 640 250" role="img" aria-label="Monthly invoiced revenue trend for the last six months">
        {[0, 1, 2, 3].map((line) => <line key={line} x1="42" x2="620" y1={32 + line * 54} y2={32 + line * 54} stroke="#dee2e6" strokeDasharray="4 4" />)}
        <polyline points={coordinates} fill="none" stroke={palette[0]} strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />
        {values.map((value, index) => <circle key={`${currency}:${index}`} cx={52 + index * 112} cy={208 - value / max * 160} r="4" fill={palette[0]}><title>{`${currency}: ${amount(String(value), currency)}`}</title></circle>)}
        {labels.map((month, index) => <text key={month} x={52 + index * 112} y="236" textAnchor="middle" fill="#6c757d" fontSize="12">{new Date(`${month}T00:00:00`).toLocaleDateString(undefined, { month: "short" })}</text>)}
      </svg>
      <div className="small text-body-secondary mt-2">Currency: {currency}</div>
    </div>
  );
}

export function FinanceManagerDashboard({ moduleName }: Readonly<{ moduleName: string }>) {
  const { bootstrap } = useBootstrap();
  const [selectedCurrency, setSelectedCurrency] = useState("");
  const [invoiceSearch, setInvoiceSearch] = useState("");
  const dashboardQuery = useQuery({
    queryKey: ["finance-manager-dashboard", bootstrap?.organization?.id],
    queryFn: async () => {
      const response = await apiClient.get<FinanceDashboardData>("/revenue-cycle/analytics/dashboard/");
      return response.data;
    },
    enabled: Boolean(bootstrap?.organization?.id),
    retry: 1,
    staleTime: 60_000,
  });
  const dashboard = dashboardQuery.data;
  const totals = dashboard?.currency_totals ?? [];
  const organizationName = bootstrap?.organization?.name ?? "Finance & Revenue Cycle";
  const activeCurrency = selectedCurrency && totals.some((row) => row.currency === selectedCurrency)
    ? selectedCurrency
    : totals[0]?.currency ?? "INR";
  const visibleTotals = selectedCurrency ? totals.filter((row) => row.currency === selectedCurrency) : totals;
  const visibleInvoices = (dashboard?.recent_invoices ?? []).filter((invoice) =>
    [invoice.invoice_number, invoice.payer_name, invoice.claim_reference, invoice.status]
      .some((value) => value.toLowerCase().includes(invoiceSearch.trim().toLowerCase())),
  );

  return (
    <section className="container-fluid py-3">
      <div className="row g-3">
        <aside className="col-12 col-xl-2">
          <nav aria-label="Finance manager navigation" className="card border-0 shadow-sm p-2 d-flex flex-row flex-xl-column gap-1 overflow-auto">
            {navigation.map(({ label, href, icon: Icon }, index) => <Link key={label} href={href} className={`d-flex align-items-center gap-2 text-decoration-none rounded px-3 py-2 text-nowrap ${index === 0 ? "bg-primary text-white" : "text-body-secondary"}`}><Icon size={17} aria-hidden="true" /><span>{label}</span></Link>)}
          </nav>
        </aside>

        <main className="col-12 col-xl-10">
          <header className="d-flex flex-wrap align-items-start justify-content-between gap-3 mb-4">
            <div><div className="small text-primary text-uppercase fw-semibold mb-2">Finance manager</div><h1 className="h2 mb-1">Good morning, Finance Manager <span aria-hidden="true">👋</span></h1><p className="text-body-secondary mb-0">{organizationName} · {moduleName}</p></div>
            <div className="d-flex flex-wrap gap-2 align-items-center"><label className="position-relative"><span className="visually-hidden">Search invoices</span><Search size={16} className="position-absolute top-50 translate-middle-y text-body-secondary" style={{ left: ".75rem" }} aria-hidden="true" /><input className="form-control form-control-sm ps-5" type="search" placeholder="Search invoice, payment…" value={invoiceSearch} onChange={(event) => setInvoiceSearch(event.target.value)} /></label><label className="small d-flex align-items-center gap-2 text-body-secondary">Currency<select className="form-select form-select-sm w-auto" aria-label="Filter finance dashboard by currency" value={selectedCurrency} onChange={(event) => setSelectedCurrency(event.target.value)}><option value="">All currencies separately</option>{totals.map((row) => <option key={row.currency} value={row.currency}>{row.currency}</option>)}</select></label></div>
          </header>

          {dashboardQuery.isError ? <div className="alert alert-danger d-flex justify-content-between align-items-center gap-2" role="alert"><span>{dashboardQuery.error instanceof Error ? dashboardQuery.error.message : "Finance dashboard data is unavailable."}</span><button className="btn btn-sm btn-outline-danger" type="button" onClick={() => void dashboardQuery.refetch()}>Retry</button></div> : null}
          {!bootstrap?.organization?.id ? <div className="alert alert-info">Select an organization to view finance metrics.</div> : null}
          {dashboardQuery.isPending && !dashboard ? <div className="alert alert-info" role="status">Loading organization finance data…</div> : null}

          <section id="revenue" aria-label="Finance summary" className="row g-3 mb-4">
            <div className="col-12 col-sm-6 col-xxl-3"><MetricCard title="Revenue this month" icon={BarChart3} rows={visibleTotals} valueKey="revenue_mtd" detail={(row) => row.revenue_change_percent === null ? "Previous month comparison unavailable" : `${row.revenue_change_percent > 0 ? "+" : ""}${row.revenue_change_percent}% vs prior month`} /></div>
            <div className="col-12 col-sm-6 col-xxl-3"><MetricCard title="Collected this month" icon={Wallet} rows={visibleTotals} valueKey="collected_mtd" detail={(row) => row.collection_rate_percent === null ? "No current-month revenue" : `${row.collection_rate_percent}% of invoiced revenue`} /></div>
            <div className="col-12 col-sm-6 col-xxl-3"><MetricCard title="Outstanding" icon={FileText} rows={visibleTotals} valueKey="outstanding" detail={() => "Open invoice balances"} /></div>
            <div className="col-12 col-sm-6 col-xxl-3"><MetricCard title="Overdue" icon={AlertTriangle} rows={visibleTotals} valueKey="overdue_amount" detail={(row) => `${row.overdue_invoice_count} overdue invoice${row.overdue_invoice_count === 1 ? "" : "s"}`} /></div>
          </section>

          <div className="row g-3 mb-4">
            <div className="col-12 col-xxl-8"><section className="card border-0 shadow-sm h-100"><div className="card-body p-3 p-lg-4"><div className="d-flex justify-content-between align-items-start gap-2 mb-3"><div><h2 className="h5 mb-1">Revenue trend</h2><p className="small text-body-secondary mb-0">Finalized invoice totals · last six months</p></div><span className="badge text-bg-light border">{dashboard?.as_of ?? "—"}</span></div>{dashboard ? <RevenueTrend data={dashboard} currency={activeCurrency} /> : <div className="placeholder-glow"><div className="placeholder col-12" style={{ height: 220 }} /></div>}</div></section></div>
            <div className="col-12 col-xxl-4"><section className="card border-0 shadow-sm h-100"><div className="card-body p-3 p-lg-4"><h2 className="h5 mb-3">Financial alerts</h2><div className="d-flex flex-column gap-3">
              <div className={`d-flex gap-3 align-items-start ${dashboard?.alerts.overdue_invoice_count ? "text-danger" : "text-success"}`}>{dashboard?.alerts.overdue_invoice_count ? <AlertTriangle size={19} aria-hidden="true" /> : <CheckCircle2 size={19} aria-hidden="true" />}<div><div className="fw-semibold">{dashboard ? dashboard.alerts.overdue_invoice_count ? `${dashboard.alerts.overdue_invoice_count} overdue invoices` : "No overdue invoices" : "Overdue invoices"}</div><div className="small text-body-secondary">{dashboard ? dashboard.alerts.overdue_invoice_count ? "Past due date with an unpaid balance" : "Invoices are within due dates" : "Loading alert status"}</div></div></div>
              <div className={`d-flex gap-3 align-items-start ${dashboard?.alerts.open_denial_count ? "text-warning-emphasis" : "text-success"}`}>{dashboard?.alerts.open_denial_count ? <AlertTriangle size={19} aria-hidden="true" /> : <CheckCircle2 size={19} aria-hidden="true" />}<div><div className="fw-semibold">{dashboard ? `${dashboard.alerts.open_denial_count} open claim denials` : "Claim denials"}</div><div className="small text-body-secondary">{dashboard ? "Open, under review, action required, or appeal pending" : "Loading alert status"}</div></div></div>
              <div className="d-flex gap-3 align-items-start text-primary"><CheckCircle2 size={19} aria-hidden="true" /><div><div className="fw-semibold">Collection performance</div><div className="small text-body-secondary">Calculated per currency from month-to-date receipts and finalized invoices.</div></div></div>
            </div></div></section></div>
          </div>

          <section className="card border-0 shadow-sm" id="reports"><div className="card-body p-3 p-lg-4"><div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3"><div><h2 className="h5 mb-1">Currency summary</h2><p className="small text-body-secondary mb-0">Amounts stay separated by currency; no cross-currency totals are combined.</p></div><span className="badge text-bg-light border">{dashboard?.period_start ?? "—"} – {dashboard?.period_end ?? "—"}</span></div>
            {visibleTotals.length ? <div className="table-responsive"><table className="table table-hover align-middle mb-0"><thead><tr><th scope="col">Currency</th><th scope="col" className="text-end">Revenue MTD</th><th scope="col" className="text-end">Collected MTD</th><th scope="col" className="text-end">Outstanding</th><th scope="col" className="text-end">Overdue</th></tr></thead><tbody>{visibleTotals.map((row) => <tr key={row.currency}><th scope="row">{row.currency}</th><td className="text-end">{amount(row.revenue_mtd, row.currency)}</td><td className="text-end">{amount(row.collected_mtd, row.currency)}</td><td className="text-end">{amount(row.outstanding, row.currency)}</td><td className="text-end">{amount(row.overdue_amount, row.currency)}</td></tr>)}</tbody></table></div> : dashboardQuery.isPending ? <p role="status" className="text-body-secondary mb-0">Loading currency summary…</p> : <p className="text-body-secondary mb-0">No finance records match this search.</p>}
          </div></section>

          <section className="card border-0 shadow-sm mt-3" id="invoices"><div className="card-body p-3 p-lg-4"><div className="d-flex flex-wrap justify-content-between align-items-start gap-2 mb-3"><div><h2 className="h5 mb-1">Recent invoices</h2><p className="small text-body-secondary mb-0">Finalized organization invoices, with current balances.</p></div><Link className="btn btn-sm btn-outline-primary" href="/workspace/billing">Open billing</Link></div>
            {visibleInvoices.length ? <div className="table-responsive"><table className="table table-hover align-middle mb-0"><thead><tr><th scope="col">Invoice</th><th scope="col">Payer</th><th scope="col">Status</th><th scope="col">Due date</th><th scope="col" className="text-end">Total</th><th scope="col" className="text-end">Balance due</th></tr></thead><tbody>{visibleInvoices.map((invoice) => <tr key={invoice.invoice_number}><th scope="row">{invoice.invoice_number}</th><td>{invoice.payer_name || "—"}</td><td><span className="badge text-bg-light border">{invoice.status.replaceAll("_", " ")}</span></td><td>{invoice.due_date ?? "—"}</td><td className="text-end">{amount(invoice.total, invoice.currency)}</td><td className="text-end">{amount(invoice.balance_due, invoice.currency)}</td></tr>)}</tbody></table></div> : dashboardQuery.isPending ? <p role="status" className="text-body-secondary mb-0">Loading invoices…</p> : <p className="text-body-secondary mb-0">No invoices match this search.</p>}
          </div></section>
        </main>
      </div>
    </section>
  );
}
