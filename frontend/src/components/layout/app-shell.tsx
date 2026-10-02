"use client";
/**
 * DatavionOS authenticated workspace presentation shell.
 *
 * This component owns presentation/layout only.
 *
 * Authorization remains backend-authoritative through:
 *
 * Identity
 *   -> Organization
 *   -> Subscription
 *   -> SaaS Entitlements
 *   -> Organization Controls
 *   -> Features
 *   -> Department Scope
 *   -> RBAC
 *   -> Effective Capability Context
 *   -> Bootstrap
 *   -> Frontend rendering
 */

import type { ReactNode } from "react";

import { AppHeader } from "./app-header";
import { AppSidebar } from "./app-sidebar";
import { RuntimeShellProvider } from "@/datavionos/runtime/components/RuntimeShellProvider";

type AppShellProps = Readonly<{
  children: ReactNode;
}>;

export function AppShell({
  children,
}: AppShellProps) {
  return (

    <div className="d-flex min-vh-100 bg-body-tertiary">
      <div className="d-none d-lg-flex flex-shrink-0">
        <RuntimeShellProvider>
      <AppSidebar />
    </RuntimeShellProvider>
      </div>

      <div className="d-flex min-vh-100 flex-column flex-grow-1 min-w-0">
        <AppHeader />

        <main className="flex-grow-1 overflow-auto">
          <div className="container-fluid px-3 px-lg-4 py-3 py-lg-4">
            {children}
          </div>
        </main>
      </div>

    </div>
  );
}
