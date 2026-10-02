"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";

function formatPrice(amount: string, currency: string): string | null {
  const numericAmount = Number(amount);
  if (!Number.isFinite(numericAmount) || !currency) return null;

  try {
    return new Intl.NumberFormat(undefined, {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(numericAmount);
  } catch {
    return `${currency} ${numericAmount.toFixed(2)}`;
  }
}

export default function BillingPage() {
  const searchParams = useSearchParams();
  const planName = searchParams.get("plan")?.trim() || "Your selected plan";
  const billingCycle = searchParams.get("cycle")?.trim();
  const price = formatPrice(
    searchParams.get("amount") ?? "",
    searchParams.get("currency") ?? "",
  );

  return (
    <main className="bg-body-tertiary">
      <div className="container py-5 py-lg-6">
        <div className="mx-auto" style={{ maxWidth: 1040 }}>
          <Link
            href="/organization/register"
            className="small text-decoration-none text-secondary"
          >
            ← Back to organization setup
          </Link>

          <div className="row g-4 g-lg-5 mt-2">
            <section className="col-lg-7" aria-labelledby="billing-heading">
              <div className="small text-primary fw-bold text-uppercase mb-3" style={{ letterSpacing: ".12em" }}>
                Signup · Billing
              </div>
              <h1 id="billing-heading" className="display-6 fw-semibold mb-3" style={{ letterSpacing: "-.04em" }}>
                Review your plan
              </h1>
              <p className="text-secondary mb-4">
                Payment is required before your organization workspace can be created.
              </p>

              <div className="border rounded-4 bg-white p-4">
                <div className="small text-secondary">Selected plan</div>
                <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mt-1">
                  <div>
                    <h2 className="h5 fw-semibold mb-1">{planName}</h2>
                    {billingCycle ? (
                      <div className="small text-secondary">
                        Billed {billingCycle.replaceAll("_", " ").toLowerCase()}
                      </div>
                    ) : null}
                  </div>
                  {price ? <div className="fs-5 fw-semibold">{price}</div> : null}
                </div>
                <div className="small text-secondary mt-3">
                  The final amount and invoice will be confirmed by DatavionOS before payment.
                </div>
              </div>

              <div className="alert alert-warning border-0 rounded-4 mt-4 mb-0" role="status">
                <div className="fw-semibold">Online checkout is not available yet</div>
                <div className="small mt-1">
                  No payment will be taken on this page. Please contact the platform team while the payment provider is being configured.
                </div>
              </div>
            </section>

            <aside className="col-lg-5" aria-label="Payment summary">
              <div className="border rounded-4 bg-white p-4">
                <h2 className="h6 fw-semibold mb-4">Payment summary</h2>
                <div className="d-flex justify-content-between gap-3 small mb-3">
                  <span className="text-secondary">Plan</span>
                  <span className="fw-semibold text-end">{planName}</span>
                </div>
                <div className="border-top pt-3 d-flex justify-content-between align-items-center gap-3">
                  <span className="fw-semibold">{price ? "Plan price" : "Amount"}</span>
                  <span className="fs-5 fw-bold">{price ?? "Confirmed at checkout"}</span>
                </div>
                <button
                  className="btn btn-primary w-100 rounded-3 py-3 mt-4"
                  type="button"
                  disabled
                  aria-describedby="checkout-unavailable"
                >
                  Checkout not available
                </button>
                <p id="checkout-unavailable" className="small text-secondary mt-3 mb-0">
                  Secure checkout will be enabled here once the payment provider is connected.
                </p>
              </div>

              <div className="small text-secondary mt-3 px-1">
                Questions about your plan? <Link href="/support" className="text-decoration-none">Contact support</Link>.
              </div>
            </aside>
          </div>
        </div>
      </div>
    </main>
  );
}
