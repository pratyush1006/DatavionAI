/**
 * Authentication context.
 */

"use client";

import { createContext } from "react";

import type { User } from "@/features/platform/accounts/domain/types";

export type AuthContextValue = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  logout: () => void;
};

export const AuthContext =
  createContext<AuthContextValue | null>(
    null,
  );
