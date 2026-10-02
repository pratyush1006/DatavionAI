"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { fetchAppointmentTracking } from "@/features/clinical/appointments/api";

const statuses = ["scheduled", "confirmed", "checked_in", "in_progress", "completed"] as const;

function displayStatus(status: string) {
  return status.replaceAll("_", " ");
}

export default function AppointmentTrackingPage() {
  const { token } = useParams<{ token: string }>();
  const query = useQuery({
    queryKey: ["appointment-tracking", token],
    queryFn: () => fetchAppointmentTracking(token),
    enabled: Boolean(token),
    refetchInterval: 5_000,
  });

  if (query.isPending) {
    return <main className="mx-auto max-w-2xl p-8">Loading your appointment status…</main>;
  }

  if (query.isError || !query.data) {
    return (
      <main className="mx-auto max-w-2xl space-y-4 p-8">
        <h1 className="text-2xl font-semibold">Appointment status unavailable</h1>
        <p>The tracking link may be invalid. Please contact the clinic for help.</p>
        <Button variant="outline" onClick={() => void query.refetch()}>Retry</Button>
      </main>
    );
  }

  const appointment = query.data;
  const currentIndex = statuses.indexOf(appointment.status as (typeof statuses)[number]);
  const isTerminalWithoutVisit = appointment.status === "cancelled" || appointment.status === "no_show";

  return (
    <main className="min-h-screen bg-muted/30 px-4 py-10">
      <section className="mx-auto max-w-2xl space-y-6 rounded-xl border bg-background p-6 shadow-sm sm:p-8">
        <header className="space-y-2">
          <p className="text-sm text-muted-foreground">DatavionOS · Patient tracking</p>
          <h1 className="text-3xl font-semibold">Your appointment</h1>
          <p className="text-sm text-muted-foreground">Appointment {appointment.appointment_number}</p>
          <Badge variant={isTerminalWithoutVisit ? "destructive" : "secondary"}>
            {displayStatus(appointment.status)}
          </Badge>
        </header>

        <div className="rounded-lg bg-muted/50 p-4">
          <p className="text-sm text-muted-foreground">Scheduled for</p>
          <p className="font-medium">
            {new Intl.DateTimeFormat("en-IN", { dateStyle: "full", timeStyle: "short" }).format(
              new Date(appointment.scheduled_start),
            )}
          </p>
        </div>

        {isTerminalWithoutVisit ? (
          <p role="status">This appointment will not proceed. Contact the clinic if you need assistance.</p>
        ) : (
          <ol className="space-y-3" aria-label="Appointment progress">
            {statuses.map((status, index) => {
              const complete = currentIndex >= index;
              return (
                <li key={status} className="flex items-center gap-3">
                  <span className={`h-3 w-3 rounded-full ${complete ? "bg-primary" : "bg-muted-foreground/30"}`} />
                  <span className={complete ? "font-medium" : "text-muted-foreground"}>
                    {displayStatus(status)}
                  </span>
                </li>
              );
            })}
          </ol>
        )}

        <div className="border-t pt-4 text-sm">
          <p>Booking deposit: <strong>{appointment.deposit_paid ? "Paid" : "Payment pending"}</strong></p>
          <p className="mt-1 text-muted-foreground">Status refreshes automatically every few seconds.</p>
        </div>
      </section>
    </main>
  );
}
