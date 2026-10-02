/**
 * Enterprise form section.
 */

import type { ReactNode } from "react";

import { Card } from "@/components/ui/card";

import { cn } from "@/lib/utils";

export type FormSectionProps =
  Readonly<{
    title: string;

    description?: string;

    children: ReactNode;

    className?: string;
  }>;

export function FormSection({
  title,
  description,
  children,
  className,
}: FormSectionProps) {
  return (
    <Card
      className={cn(
        "space-y-6",
        className,
      )}
    >
      <div>
        <h3 className="text-lg font-semibold">
          {title}
        </h3>

        {description && (
          <p className="mt-1 text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>

      {children}
    </Card>
  );
}
