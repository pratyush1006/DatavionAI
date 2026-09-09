/**
 * =============================================================================
 * DatavionOS
 * File: src/components/layout/user-menu.tsx
 * =============================================================================
 *
 * Authenticated user menu.
 *
 * Responsibilities
 * ----------------
 * - Display the authenticated user's identity.
 * - Provide the logout action.
 * - Delegate authentication state changes to the canonical auth runtime.
 *
 * Authentication ownership remains in:
 *
 *     @/core/auth
 *
 * This component does not own authentication state or storage.
 * =============================================================================
 */

"use client";

import {
  LogOut,
  User,
} from "lucide-react";

import {
  Avatar,
  AvatarFallback,
} from "@/components/ui/avatar";

import {
  Button,
} from "@/components/ui/button";

import {
  useAuth,
} from "@/core/auth";

export function UserMenu() {
  const {
    user,
    logout,
    isLoading,
  } = useAuth();

  const displayName =
    user
      ? [
          user.first_name,
          user.last_name,
        ]
          .filter(Boolean)
          .join(" ")
      : "";

  const initials =
    displayName
      ? displayName
          .split(/\s+/)
          .map(
            (part) =>
              part.charAt(0),
          )
          .join("")
          .slice(0, 2)
          .toUpperCase()
      : null;

  const handleLogout =
    async (): Promise<void> => {
      await logout();
    };

  return (
    <div className="flex items-center gap-2">
      <div className="hidden text-right sm:block">
        {displayName ? (
          <p className="text-sm font-medium leading-none">
            {displayName}
          </p>
        ) : null}

        {user?.email ? (
          <p className="mt-1 text-xs text-muted-foreground">
            {user.email}
          </p>
        ) : null}
      </div>

      <Avatar>
        <AvatarFallback>
          {initials ? (
            initials
          ) : (
            <User className="h-4 w-4" />
          )}
        </AvatarFallback>
      </Avatar>

      <Button
        type="button"
        variant="ghost"
        size="sm"
        onClick={handleLogout}
        disabled={isLoading}
        aria-label="Log out"
      >
        <LogOut className="h-4 w-4" />
        <span className="hidden md:inline">
          {isLoading
            ? "Signing out..."
            : "Sign out"}
        </span>
      </Button>
    </div>
  );
}
