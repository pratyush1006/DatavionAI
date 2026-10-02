/**
 * Enterprise application form.
 */

"use client";

import type {
  FormEventHandler,
  ReactNode,
} from "react";

import { cn } from "@/lib/utils";

export type AppFormProps = Readonly<{
  children: ReactNode;

  onSubmit: FormEventHandler<HTMLFormElement>;

  className?: string;
}>;

export function AppForm({
  children,
  onSubmit,
  className,
}: AppFormProps) {
  return (
    <form
      noValidate
      onSubmit={onSubmit}
      className={cn(
        "space-y-6",
        className,
      )}
    >
      {children}
    </form>
  );
}
