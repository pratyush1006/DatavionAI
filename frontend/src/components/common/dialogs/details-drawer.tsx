/**
 * ----------------------------------------------------------------------
 * Details Drawer
 * ----------------------------------------------------------------------
 *
 * Purpose:
 * Enterprise drawer for displaying entity details without
 * leaving the current page.
 *
 * Used By:
 * - Organizations
 * - Departments
 * - Teams
 * - Users
 * - Patients
 * - Laboratories
 * - Billing
 *
 * ----------------------------------------------------------------------
 */

"use client";

import type { ReactNode } from "react";

import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";

import { cn } from "@/lib/utils";

export type DetailsDrawerProps = Readonly<{
  open: boolean;

  onOpenChange: (
    open: boolean,
  ) => void;

  title: string;

  description?: string;

  children: ReactNode;

  footer?: ReactNode;

  width?: "sm" | "md" | "lg";

  className?: string;
}>;

const WIDTH_CLASSES = {
  sm: "sm:max-w-md",
  md: "sm:max-w-xl",
  lg: "sm:max-w-2xl",
} as const;

export function DetailsDrawer({
  open,
  onOpenChange,
  title,
  description,
  children,
  footer,
  width = "md",
  className,
}: DetailsDrawerProps) {
  return (
    <Sheet
      open={open}
      onOpenChange={onOpenChange}
    >
      <SheetContent
        side="right"
        className={cn(
          "flex h-full flex-col p-0",
          WIDTH_CLASSES[width],
          className,
        )}
      >
        <SheetHeader className="border-b px-6 py-5">
          <SheetTitle>
            {title}
          </SheetTitle>

          {description && (
            <SheetDescription>
              {description}
            </SheetDescription>
          )}
        </SheetHeader>

        <div className="flex-1 overflow-y-auto px-6 py-6">
          {children}
        </div>

        {footer && (
          <div className="border-t bg-muted/30 px-6 py-4">
            {footer}
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
