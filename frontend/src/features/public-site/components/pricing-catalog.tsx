"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchPublicSaaSPlans,
  type PublicSaaSPlan,
} from "@/features/public-site/api/pricing";

function money(value: string | number, currency: string) {
  const amount = Number(value);
  if (!Number.isFinite(amount)) return `${value} ${currency}`;
  try {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      maximumFractionDigits: 0,
    }).format(amount);
  } catch {
    return `${amount.toFixed(0)} ${currency}`;
  }
}

function humanize(value: string) {
  return value.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function PricingCatalog() {
  const [plans, setPlans] = useState<PublicSaaSPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    void fetchPublicSaaSPlans()
      .then((data) => {
        if (!cancelled) setPlans(data);
      })
      .catch(() => {
        if (!cancelled) setError("Unable to load the current plan catalog.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <div className="rounded-2xl border p-10 text-center text-sm text-muted-foreground">Loading current plans...</div>;
  }
  if (error) {
    return <div className="rounded-2xl border p-10 text-center text-sm text-muted-foreground">{error}</div>;
  }
  if (!plans.length) {
    return <div className="rounded-2xl border p-10 text-center text-sm text-muted-foreground">No public plans are currently available.</div>;
  }

  return (
    <div className="grid gap-5 lg:grid-cols-3">
      {plans.map((plan) => (
        <article key={plan.code} className="relative flex flex-col rounded-2xl border p-6">
          {plan.is_featured ? (
            <span className="absolute right-5 top-5 rounded-full bg-primary/10 px-2.5 py-1 text-[11px] font-semibold text-primary">Featured</span>
          ) : null}
          <p className="pr-20 text-lg font-semibold">{plan.name}</p>
          <p className="mt-1 text-xs text-muted-foreground">{humanize(plan.healthcare_segment)}</p>
          <div className="mt-6">
            <span className="text-3xl font-bold">{money(plan.price, plan.currency)}</span>
            <span className="ml-1 text-xs text-muted-foreground">/ {humanize(plan.billing_cycle)}</span>
          </div>
          <p className="mt-4 min-h-12 text-sm leading-6 text-muted-foreground">{plan.description}</p>
          {plan.trial_days > 0 ? <p className="mt-4 text-xs font-medium">{plan.trial_days}-day trial</p> : null}
          <Link href="/register" className="mt-auto pt-7 text-center rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground">
            Get started
          </Link>
        </article>
      ))}
    </div>
  );
}
