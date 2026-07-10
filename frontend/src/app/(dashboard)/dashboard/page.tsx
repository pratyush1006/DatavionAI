import { AppShell } from "@/components/layout/app-shell";
export default function DashboardPage() {
  return (
    <AppShell>
      <div>
        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="mt-2 text-muted-foreground">
          Welcome to Datavion AI.
        </p>
      </div>
    </AppShell>
  );
}
