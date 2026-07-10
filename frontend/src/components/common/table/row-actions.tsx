/**
 * Enterprise row actions.
 */

"use client";

import type { ReactNode } from "react";

import { MoreHorizontal } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { cn } from "@/lib/utils";

export type RowActionsProps = Readonly<{
  children: ReactNode;

  className?: string;

  menuClassName?: string;
}>;

export function RowActions({
  children,
  className,
  menuClassName,
}: RowActionsProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        aria-label="Row actions"
        className={cn(
            buttonVariants({
            variant: "ghost",
            size: "icon-sm",
            }),
            className,
        )}
    >
            <MoreHorizontal className="size-4" />
        </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        sideOffset={6}
        className={cn(
          "w-52",
          menuClassName,
        )}
      >
        {children}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
