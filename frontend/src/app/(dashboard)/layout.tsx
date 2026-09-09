/**
 * =============================================================================
 * DatavionOS
 * File: src/app/(dashboard)/layout.tsx
 * =============================================================================
 *
 * Protected application workspace layout.
 *
 * Responsibilities
 * ----------------
 * - Wait for authentication initialization.
 * - Protect dashboard routes from unauthenticated access.
 * - Render the application shell for authenticated users.
 *
 * Important
 * ---------
 * Authentication initialization is distinct from authentication loading.
 *
 * We MUST NOT redirect while:
 *
 *     isInitialized === false
 *
 * because the authentication provider has not yet determined whether a valid
 * session exists.
 * =============================================================================
 */

"use client";

import {
  useEffect,
} from "react";

import {
  useRouter,
} from "next/navigation";

import {
  AppShell,
} from "@/components/layout/app-shell";

import {
  useAuth,
} from "@/core/auth";

export default function DashboardLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const router =
    useRouter();

  const {
    isAuthenticated,
    isInitialized,
    isLoading,
  } = useAuth();

  /* ===========================================================================
   * Authentication Guard
   * =========================================================================== */

  useEffect(() => {
    /*
     * Never redirect before authentication initialization has completed.
     *
     * On the initial render:
     *
     *     isInitialized === false
     *
     * isAuthenticated cannot yet be trusted.
     */
    if (
      !isInitialized
    ) {
      return;
    }

    /*
     * Once initialization has completed, an unauthenticated user is sent
     * back to the login page.
     */
    if (
      !isAuthenticated
    ) {
      router.replace(
        "/login",
      );
    }
  }, [
    isAuthenticated,
    isInitialized,
    router,
  ]);

  /* ===========================================================================
   * Initialization / Loading State
   * =========================================================================== */

  /*
   * Authentication has not finished restoring the current session.
   */
  if (
    !isInitialized
  ) {
    return (
      <main className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
        Loading secure workspace...
      </main>
    );
  }

  /*
   * An authentication operation is currently running.
   */
  if (
    isLoading
  ) {
    return (
      <main className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
        Loading secure workspace...
      </main>
    );
  }

  /*
   * Initialization is complete and there is no authenticated session.
   *
   * The effect above is responsible for navigation to /login.
   */
  if (
    !isAuthenticated
  ) {
    return (
      <main className="flex min-h-screen items-center justify-center text-sm text-muted-foreground">
        Redirecting to sign in...
      </main>
    );
  }

  /* ===========================================================================
   * Authenticated Workspace
   * =========================================================================== */

  return (
    <AppShell>
      {children}
    </AppShell>
  );
}
