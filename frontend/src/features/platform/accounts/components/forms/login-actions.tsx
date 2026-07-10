/**
 * Login form actions.
 */

"use client";

import { Loader2, LogIn } from "lucide-react";

import { Button } from "@/components/ui/button";

export type LoginActionsProps = Readonly<{
  isSubmitting?: boolean;
}>;

export function LoginActions({
  isSubmitting = false,
}: LoginActionsProps) {
  return (
    <div className="flex justify-end pt-6">

      <Button
        type="submit"
        disabled={isSubmitting}
        className="w-full"
      >
        {isSubmitting ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />

            Signing in...
          </>
        ) : (
          <>
            <LogIn className="mr-2 h-4 w-4" />

            Sign In
          </>
        )}
      </Button>

    </div>
  );
}
