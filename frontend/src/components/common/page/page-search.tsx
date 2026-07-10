/**
 * Enterprise page search input.
 */

"use client";

import { Search, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { cn } from "@/lib/utils";

export type PageSearchProps = Readonly<{
  value: string;

  onChange: (
    value: string,
  ) => void;

  placeholder?: string;

  disabled?: boolean;

  className?: string;
}>;

export function PageSearch({
  value,
  onChange,
  placeholder = "Search...",
  disabled = false,
  className,
}: PageSearchProps) {
  return (
    <div
      className={cn(
        "relative w-full lg:max-w-md",
        className,
      )}
    >
      <Search
        className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
      />

      <Input
        value={value}
        disabled={disabled}
        placeholder={placeholder}
        className="pl-10 pr-10"
        onChange={(event) =>
          onChange(event.target.value)
        }
      />

      {value.length > 0 && (
        <Button
          type="button"
          size="icon-sm"
          variant="ghost"
          aria-label="Clear search"
          className="absolute right-1 top-1/2 -translate-y-1/2"
          onClick={() => onChange("")}
        >
          <X className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
}
