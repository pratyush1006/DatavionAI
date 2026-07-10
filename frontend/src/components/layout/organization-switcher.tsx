/**
 * Organization switcher.
 */

import { Building2 } from "lucide-react";

import { Button } from "@/components/ui/button";

export function OrganizationSwitcher() {
  return (
    <Button
      variant="outline"
      className="gap-2"
    >
      <Building2 className="h-4 w-4" />

      Datavion Demo Hospital
    </Button>
  );
}
