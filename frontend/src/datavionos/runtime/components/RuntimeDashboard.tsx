 "use client";

import { useRuntimeShell } from "./RuntimeShellProvider";
import {
  hasCapability,
  hasModule,
} from "../lib/capability";

const CARDS = [
  {
    id: "patients",
    label: "Patients",
    module: "patient_management",
  },
  {
    id: "appointments",
    label: "Appointments",
    module: "appointments",
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    module: "pharmacy",
  },
  {
    id: "laboratory",
    label: "Laboratory",
    module: "laboratory",
  },
  {
    id: "imaging",
    label: "Imaging",
    module: "imaging",
  },
  {
    id: "billing",
    label: "Billing",
    module: "billing",
  },
];

export function RuntimeDashboard() {
  const {
    context,
    loading,
    error,
    refresh,
  } = useRuntimeShell();

  if (loading) {
    return <main style={{ padding: 32 }}>Loading dashboard...</main>;
  }

  if (error || !context) {
    return (
      <main style={{ padding: 32 }}>
        <h1>DatavionOS</h1>
        <p>{error ?? "Runtime context unavailable."}</p>

        <button
          type="button"
          onClick={() => void refresh()}
          style={{
            padding: "10px 16px",
            borderRadius: 8,
            border: "1px solid #d1d5db",
            background: "#ffffff",
            cursor: "pointer",
          }}
        >
          Retry
        </button>
      </main>
    );
  }

  const visibleCards = CARDS.filter(
    (card) =>
      hasModule(context, card.module) ||
      hasCapability(context, `${card.module}.view`),
  );

  return (
    <main
      style={{
        flex: 1,
        padding: 32,
        background: "#f8fafc",
      }}
    >
      <div style={{ marginBottom: 28 }}>
        <h1
          style={{
            margin: 0,
            fontSize: 30,
            fontWeight: 700,
          }}
        >
          Dashboard
        </h1>

        <p style={{ color: "#64748b" }}>
          Generated from the effective DatavionOS capability context.
        </p>
      </div>

      <section
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 16,
        }}
      >
        {visibleCards.map((card) => (
          <article
            key={card.id}
            style={{
              background: "#ffffff",
              border: "1px solid #e5e7eb",
              borderRadius: 12,
              padding: 20,
            }}
          >
            <div
              style={{
                fontSize: 14,
                color: "#64748b",
                marginBottom: 8,
              }}
            >
              Enabled module
            </div>

            <div
              style={{
                fontSize: 20,
                fontWeight: 700,
              }}
            >
              {card.label}
            </div>
          </article>
        ))}
      </section>

      {visibleCards.length === 0 && (
        <section
          style={{
            marginTop: 24,
            padding: 24,
            background: "#ffffff",
            border: "1px solid #e5e7eb",
            borderRadius: 12,
          }}
        >
          No organization modules are currently enabled.
        </section>
      )}
    </main>
  );
}
