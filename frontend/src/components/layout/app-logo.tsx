/**
 * Application logo.
 */

import { Activity } from "lucide-react";

export function AppLogo() {
  return (
    <div className="flex items-center gap-3">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-primary-foreground">
        <Activity className="h-5 w-5" />
      </div>

      <div>
        <h1 className="text-lg font-bold">
          Datavion AI
        </h1>

        <p className="text-xs text-muted-foreground">
          Healthcare OS
        </p>
      </div>
    </div>
  );
}
