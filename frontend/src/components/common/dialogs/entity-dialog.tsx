/**
 * ----------------------------------------------------------------------
 * Entity Dialog
 * ----------------------------------------------------------------------
 *
 * Purpose:
 * Standard dialog wrapper for Create, Edit and View operations.
 *
 * Used By:
 * - Organizations
 * - Departments
 * - Teams
 * - Users
 * - Patients
 * - Laboratories
 * - Billing
 * ----------------------------------------------------------------------
 */

"use client";

import type { ReactNode } from "react";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { cn } from "@/lib/utils";

export type EntityDialogProps = Readonly<{
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}>;

const SIZE_CLASSES = {
  sm: "sm:max-w-lg",
  md: "sm:max-w-3xl",
  lg: "sm:max-w-5xl",
  xl: "sm:max-w-7xl",
} as const;

export function EntityDialog({
  open,
  onOpenChange,
  title,
  description,
  children,
  footer,
  size = "lg",
  className,
}: EntityDialogProps) {
  return (
    <Dialog
      open={open}
      onOpenChange={onOpenChange}
    >
      <DialogContent
        className={cn(
          "flex max-h-[92vh] flex-col overflow-hidden p-0",
          SIZE_CLASSES[size],
          className,
        )}
      >
        <DialogHeader className="border-b px-8 py-6">
          <DialogTitle className="text-xl">
            {title}
          </DialogTitle>

          {description && (
            <DialogDescription>
              {description}
            </DialogDescription>
          )}
        </DialogHeader>

        <div className="flex-1 overflow-y-auto px-8 py-6">
          {children}
        </div>

        {footer && (
          <div className="border-t bg-muted/40 px-8 py-4">
            {footer}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
