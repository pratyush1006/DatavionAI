/**
 * Enterprise data table search.
 */

"use client";

import { Search } from "lucide-react";

import { Input } from "@/components/ui/input";

import { cn } from "@/lib/utils";

export type DataTableSearchProps = Readonly<{
  value: string;

  onChange: (
    value: string,
  ) => void;

  placeholder?: string;

  className?: string;
}>;

export function DataTableSearch({
  value,
  onChange,
  placeholder = "Search...",
  className,
}: DataTableSearchProps) {
  return (
    <div
      className={cn(
        "relative w-full max-w-sm",
        className,
      )}
    >
      <Search
        className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
      />

      <Input
        value={value}
        placeholder={placeholder}
        className="pl-10"
        onChange={(event) =>
          onChange(
            event.target.value,
          )
        }
      />
    </div>
  );
}
