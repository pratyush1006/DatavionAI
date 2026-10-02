"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

import { DashboardShell } from "@/components/datavionos/dashboard-shell";
import { DynamicModuleWorkspace } from "@/components/workspace/dynamic-module-workspace";
import { useAuth } from "@/core/auth";

// These modules already have real, backend-connected application pages.
// Keep the backend contracts on /workspace/:module compatible while sending
// users to the operational UI rather than the metadata fallback.
const OPERATIONAL_ROUTES: Readonly<Record<string, string>> = {
  departments: "/settings/access",
  teams: "/settings/access",
  employees: "/employees",
  documents: "/documents",
  notes: "/notes",
  transcription: "/transcription",
  patients: "/patients",
  appointments: "/clinical/appointments",
};

/**
 * Canonical entry point for backend-provided /workspace/:module routes.
 * The workspace validates the requested module against the authenticated
 * user's current backend bootstrap capability context.
 */
export default function WorkspaceModulePage() {
  const params = useParams<{ module: string }>();
  const router = useRouter();
  const { isAuthenticated, isInitialized, isLoading } = useAuth();
  const moduleIdentifier = String(params.module ?? "");
  const operationalRoute = OPERATIONAL_ROUTES[moduleIdentifier.toLowerCase()];

  useEffect(() => {
    if (isInitialized && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, isInitialized, router]);

  useEffect(() => {
    if (isInitialized && isAuthenticated && operationalRoute) {
      router.replace(operationalRoute);
    }
  }, [isAuthenticated, isInitialized, operationalRoute, router]);

  if (!isInitialized || isLoading) {
    return (
      <main className="container-fluid py-4" aria-busy="true">
        Loading secure workspace...
      </main>
    );
  }

  if (!isAuthenticated) {
    return (
      <main className="container-fluid py-4" aria-busy="true">
        Redirecting to sign in...
      </main>
    );
  }

  if (operationalRoute) {
    return <main className="container-fluid py-4" aria-busy="true">Opening module workspace…</main>;
  }

  return (
    <DashboardShell>
      <DynamicModuleWorkspace moduleIdentifier={moduleIdentifier} />
    </DashboardShell>
  );
}
