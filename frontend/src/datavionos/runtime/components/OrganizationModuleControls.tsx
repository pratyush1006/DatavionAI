"use client";

import { useState } from "react";

import {
  hasModule,
  isOrganizationAdmin,
} from "../lib/capability";

import {
  updateOrganizationModuleState,
} from "../lib/capability-client";

import {
  useRuntimeShell,
} from "./RuntimeShellProvider";

const MODULES = [
  "patient_management",
  "appointments",
  "pharmacy",
  "laboratory",
  "imaging",
  "billing",
  "telemedicine",
];

export function OrganizationModuleControls() {
  const {
    context,
    refresh,
  } = useRuntimeShell();

  const [busy, setBusy] = useState<string | null>(null);

  if (!context || !isOrganizationAdmin(context)) {
    return null;
  }

  async function toggle(
    moduleKey: string,
    enabled: boolean,
  ) {
    setBusy(moduleKey);

    try {
      await updateOrganizationModuleState(
        moduleKey,
        { enabled },
      );

      await refresh();
    } finally {
      setBusy(null);
    }
  }

  return (
    <section
      style={{
        marginTop: 32,
        background: "#ffffff",
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 24,
      }}
    >
      <h2
        style={{
          marginTop: 0,
          fontSize: 20,
        }}
      >
        Organization Modules
      </h2>

      <p style={{ color: "#64748b" }}>
        Organization administrators can enable or disable
        modules within the capabilities allowed by the
        organization subscription.
      </p>

      <div
        style={{
          display: "grid",
          gap: 12,
        }}
      >
        {MODULES.map((moduleKey) => {
          const enabled = hasModule(
            context,
            moduleKey,
          );

          return (
            <div
              key={moduleKey}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: 12,
                border: "1px solid #e5e7eb",
                borderRadius: 8,
              }}
            >
              <span>{moduleKey}</span>

              <button
                type="button"
                disabled={busy === moduleKey}
                onClick={() =>
                  void toggle(
                    moduleKey,
                    !enabled,
                  )
                }
                style={{
                  padding: "8px 14px",
                  borderRadius: 8,
                  border: "1px solid #d1d5db",
                  cursor:
                    busy === moduleKey
                      ? "wait"
                      : "pointer",
                }}
              >
                {busy === moduleKey
                  ? "Saving..."
                  : enabled
                    ? "Enabled"
                    : "Disabled"}
              </button>
            </div>
          );
        })}
      </div>
    </section>
  );
}
