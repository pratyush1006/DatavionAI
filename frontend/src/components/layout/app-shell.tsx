/**
 * Enterprise application shell.
 */

import type { ReactNode } from "react";

import { AppHeader } from "./app-header";
import { AppSidebar } from "./app-sidebar";

type AppShellProps = Readonly<{
  children: ReactNode;
}>;

export function AppShell({
  children,
}: AppShellProps) {
  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar />

      <div className="flex min-h-screen flex-1 flex-col">
        <AppHeader />

        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
