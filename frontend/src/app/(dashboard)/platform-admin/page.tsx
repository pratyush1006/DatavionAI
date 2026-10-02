"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  BadgeIndianRupee,
  Building2,
  CheckCircle2,
  CircleAlert,
  CreditCard,
  HeartPulse,
  ServerCog,
  Users,
} from "lucide-react";

import { apiClient } from "@/core/api";
import { useBootstrap } from "@/core/bootstrap";

type Tenant = Readonly<{
  id: string;
  name: string;
  slug: string;
  tenant_type: string;
  status: string;
}>;

type Overview = Readonly<{
  generated_at: string;
  organizations: { total: number; active: number; growth_percent: number | null };
  users: { total: number; active: number };
  subscriptions: { active: number; trial: number; past_due: number };
  revenue: { collected: Array<{ currency: string; amount: string; invoice_count: number }> };
  system: {
    healthy: boolean;
    checks: Record<string, { healthy: boolean; message: string; duration_ms?: number }>;
  };
  recent_organizations: Tenant[];
}>;

async function fetchTenants(): Promise<Tenant[]> {
  return (await apiClient.get<Tenant[]>("/tenancy/tenants/")).data;
}

async function fetchOverview(): Promise<Overview> {
  return (await apiClient.get<Overview>("/tenancy/platform-overview/")).data;
}

function greetingFor(hour: number): string {
  return hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
}

function MetricCard({ icon: Icon, label, value, detail, tone = "primary" }: Readonly<{
  icon: typeof Building2;
  label: string;
  value: string | number;
  detail: string;
  tone?: "primary" | "success" | "info" | "warning";
}>) {
  return <article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-start gap-3"><div><div className="small text-uppercase fw-semibold text-body-secondary" style={{ letterSpacing: ".06em" }}>{label}</div><div className="fs-3 fw-bold mt-2">{value}</div><div className="small text-body-secondary mt-1">{detail}</div></div><div className={`rounded-3 p-2 bg-${tone}-subtle text-${tone}`}><Icon size={22} aria-hidden="true" /></div></div></div></article>;
}

export default function PlatformAdminPage() {
  const { bootstrap, isLoading: isBootstrapLoading } = useBootstrap();
  const isPlatformAdmin = Boolean(bootstrap?.user.is_platform_admin);
  const enabled = isPlatformAdmin && !isBootstrapLoading;
  const overviewQuery = useQuery({ queryKey: ["platform-admin", "overview"], queryFn: fetchOverview, enabled, refetchInterval: 60_000 });
  const tenantsQuery = useQuery({ queryKey: ["platform-admin", "tenants"], queryFn: fetchTenants, enabled });

  if (isBootstrapLoading) return <main className="container-fluid py-4" aria-busy="true">Loading platform administration…</main>;
  if (!isPlatformAdmin) return <main className="container-fluid py-4"><div className="alert alert-danger" role="alert">Platform administrator access is required for this workspace.</div></main>;

  const overview = overviewQuery.data;
  const tenants = tenantsQuery.data ?? overview?.recent_organizations ?? [];
  const displayName = bootstrap?.user.full_name?.trim() || [bootstrap?.user.first_name, bootstrap?.user.last_name].filter(Boolean).join(" ") || "Platform administrator";
  const collected = overview?.revenue.collected ?? [];
  const primaryCollection = collected.length === 1 ? collected[0] : undefined;
  const revenue = primaryCollection ? new Intl.NumberFormat(undefined, { style: "currency", currency: primaryCollection.currency || "INR", maximumFractionDigits: 0 }).format(Number(primaryCollection.amount)) : collected.length ? "Multi-currency" : "No collections";
  const healthChecks = Object.entries(overview?.system.checks ?? {});

  return (
    <main className="container-fluid py-4 py-lg-5">
      <header className="d-flex flex-column flex-xl-row justify-content-between gap-3 mb-4 mb-lg-5">
        <div><div className="small text-uppercase fw-semibold text-primary mb-2" style={{ letterSpacing: ".08em" }}>DatavionOS control plane</div><h1 className="h2 fw-bold mb-2">{greetingFor(new Date().getHours())}, {displayName}</h1><p className="text-body-secondary mb-0">Here&apos;s the current health of the DatavionOS platform.</p></div>
        <div className="small text-body-secondary align-self-xl-end">{overview?.generated_at ? `Updated ${new Date(overview.generated_at).toLocaleString()}` : "Loading live platform metrics…"}</div>
      </header>

      {overviewQuery.isError ? <div className="alert alert-warning">Platform metrics could not be loaded. Tenant management remains available.</div> : null}

      <section className="row g-3 mb-4" aria-label="Platform key performance indicators">
        <div className="col-12 col-sm-6 col-xl-3"><MetricCard icon={Building2} label="Organizations" value={overviewQuery.isLoading ? "…" : overview?.organizations.total ?? 0} detail={overview?.organizations.growth_percent === null || overview?.organizations.growth_percent === undefined ? `${overview?.organizations.active ?? 0} active` : `${overview.organizations.growth_percent >= 0 ? "+" : ""}${overview.organizations.growth_percent}% this month`} /></div>
        <div className="col-12 col-sm-6 col-xl-3"><MetricCard icon={Users} label="Users" value={overviewQuery.isLoading ? "…" : overview?.users.total ?? 0} detail={`${overview?.users.active ?? 0} active accounts`} tone="info" /></div>
        <div className="col-12 col-sm-6 col-xl-3"><MetricCard icon={BadgeIndianRupee} label="Collected revenue" value={overviewQuery.isLoading ? "…" : revenue} detail={primaryCollection ? `${primaryCollection.invoice_count} settled invoices this month` : "Paid invoice totals only"} tone="success" /></div>
        <div className="col-12 col-sm-6 col-xl-3"><MetricCard icon={HeartPulse} label="System" value={overviewQuery.isLoading ? "…" : overview?.system.healthy ? "Healthy" : "Attention"} detail={overview?.system.healthy ? "All registered checks passing" : "One or more checks need review"} tone={overview?.system.healthy ? "success" : "warning"} /></div>
      </section>

      <section className="row g-3 mb-4">
        <div className="col-12 col-xl-7"><article id="activity" className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-center gap-3 mb-4"><div><h2 className="h5 mb-1">Platform activity</h2><p className="small text-body-secondary mb-0">Live operational totals from the control plane.</p></div><Activity className="text-primary" aria-hidden="true" /></div><div className="row g-3"><div className="col-12 col-md-4"><div className="rounded-3 bg-body-tertiary p-3"><div className="small text-body-secondary">Active organizations</div><div className="fs-4 fw-bold mt-1">{overview?.organizations.active ?? "—"}</div></div></div><div className="col-12 col-md-4"><div className="rounded-3 bg-body-tertiary p-3"><div className="small text-body-secondary">Active subscriptions</div><div className="fs-4 fw-bold mt-1">{overview?.subscriptions.active ?? "—"}</div></div></div><div className="col-12 col-md-4"><div className="rounded-3 bg-body-tertiary p-3"><div className="small text-body-secondary">Past due subscriptions</div><div className="fs-4 fw-bold mt-1">{overview?.subscriptions.past_due ?? "—"}</div></div></div></div><p className="small text-body-secondary mt-4 mb-0">Historical growth charts will appear once the platform metric snapshot job is configured; no trend data is fabricated.</p></div></article></div>
        <div className="col-12 col-xl-5"><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-center gap-3 mb-3"><div><h2 className="h5 mb-1">System health</h2><p className="small text-body-secondary mb-0">Backend readiness checks.</p></div><ServerCog className="text-primary" aria-hidden="true" /></div>{healthChecks.length ? <div className="vstack gap-3">{healthChecks.map(([key, check]) => <div key={key} className="d-flex align-items-start justify-content-between gap-3"><div className="d-flex gap-2"><span className={check.healthy ? "text-success" : "text-warning"}>{check.healthy ? <CheckCircle2 size={18} aria-hidden="true" /> : <CircleAlert size={18} aria-hidden="true" />}</span><div><div className="fw-semibold text-capitalize">{key}</div><div className="small text-body-secondary">{check.message}</div></div></div><span className="small text-body-secondary">{check.duration_ms !== undefined ? `${check.duration_ms} ms` : check.healthy ? "Healthy" : "Review"}</span></div>)}</div> : <div className="small text-body-secondary">Loading registered health checks…</div>}</div></article></div>
      </section>

      <section className="row g-3">
        <div className="col-12 col-xl-7"><article className="card border-0 shadow-sm h-100"><div className="card-body p-4"><div className="d-flex justify-content-between align-items-center gap-3 mb-3"><div><h2 className="h5 mb-1">Organizations</h2><p className="small text-body-secondary mb-0">Most recently created platform tenants.</p></div><Link href="/organizations" className="btn btn-outline-primary btn-sm">Manage organizations</Link></div><div className="table-responsive"><table className="table align-middle mb-0"><thead><tr><th>Name</th><th>Type</th><th>Status</th></tr></thead><tbody>{tenants.slice(0, 8).map((tenant) => <tr key={tenant.id}><td><div className="fw-semibold">{tenant.name}</div><div className="small text-body-secondary">{tenant.slug}</div></td><td className="text-capitalize">{tenant.tenant_type}</td><td><span className={`badge ${tenant.status.toLowerCase() === "active" ? "text-bg-success" : "text-bg-secondary"}`}>{tenant.status}</span></td></tr>)}{!tenants.length && !tenantsQuery.isLoading ? <tr><td colSpan={3} className="text-body-secondary">No organizations found.</td></tr> : null}</tbody></table></div></div></article></div>
        <div className="col-12 col-xl-5"><article id="billing" className="card border-0 shadow-sm h-100"><div className="card-body p-4"><h2 className="h5 mb-1">Subscription operations</h2><p className="small text-body-secondary mb-4">Commercial lifecycle across all organizations.</p><div className="vstack gap-3"><div className="d-flex justify-content-between"><span>Active</span><strong>{overview?.subscriptions.active ?? "—"}</strong></div><div className="d-flex justify-content-between"><span>Trial</span><strong>{overview?.subscriptions.trial ?? "—"}</strong></div><div className="d-flex justify-content-between"><span>Past due</span><strong className={overview?.subscriptions.past_due ? "text-warning" : undefined}>{overview?.subscriptions.past_due ?? "—"}</strong></div></div><div className="border-top mt-4 pt-3"><Link href="/organization/subscription" className="btn btn-outline-primary btn-sm"><CreditCard size={16} className="me-1" aria-hidden="true" />Subscription settings</Link></div></div></article></div>
      </section>
    </main>
  );
}
