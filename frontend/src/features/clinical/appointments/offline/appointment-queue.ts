import Dexie, { type Table } from "dexie";
import type { Appointment, AppointmentFormValues } from "../domain";
import { createAppointmentRequest } from "../api";

export type OfflineAppointmentStatus = "queued" | "syncing" | "synced" | "failed";

export type OfflineAppointmentEntry = {
  idempotencyKey: string;
  values: AppointmentFormValues;
  status: OfflineAppointmentStatus;
  createdAt: string;
  error: string;
  appointment?: Appointment;
};

class OfflineAppointmentDatabase extends Dexie {
  appointments!: Table<OfflineAppointmentEntry, string>;

  constructor() {
    super("datavion-clinical-appointments");
    this.version(1).stores({
      appointments: "idempotencyKey,status,createdAt",
    });
  }
}

let database: OfflineAppointmentDatabase | undefined;
let activeSync: Promise<void> | undefined;

function getDatabase() {
  database ??= new OfflineAppointmentDatabase();
  return database;
}

export async function enqueueOfflineAppointment(
  values: AppointmentFormValues,
): Promise<OfflineAppointmentEntry> {
  const entry: OfflineAppointmentEntry = {
    idempotencyKey: crypto.randomUUID(),
    // Avoid persisting free-text clinical/scheduling notes on the device while offline.
    values: { ...values, reason: "", notes: "", meetingUrl: "" },
    status: "queued",
    createdAt: new Date().toISOString(),
    error: "",
  };
  await getDatabase().appointments.add(entry);
  return entry;
}

export async function listOfflineAppointments(): Promise<OfflineAppointmentEntry[]> {
  return getDatabase().appointments.orderBy("createdAt").reverse().toArray();
}

export async function retryOfflineAppointment(idempotencyKey: string): Promise<void> {
  await getDatabase().appointments.update(idempotencyKey, {
    status: "queued",
    error: "",
  });
}

export async function updateOfflineAppointment(
  idempotencyKey: string,
  appointment: Appointment,
): Promise<void> {
  await getDatabase().appointments.update(idempotencyKey, { appointment });
}

export async function synchronizeOfflineAppointments(): Promise<void> {
  if (typeof navigator === "undefined" || !navigator.onLine) return;
  if (activeSync) return activeSync;

  activeSync = (async () => {
    const table = getDatabase().appointments;
    await table.where("status").equals("syncing").modify({ status: "queued" });
    const queued = await table.where("status").equals("queued").sortBy("createdAt");
    for (const entry of queued) {
      if (!navigator.onLine) break;
      await table.update(entry.idempotencyKey, { status: "syncing", error: "" });
      try {
        const appointment = await createAppointmentRequest(
          entry.values,
          entry.idempotencyKey,
        );
        await table.update(entry.idempotencyKey, {
          status: "synced",
          appointment,
          error: "",
        });
      } catch (cause) {
        const online = navigator.onLine;
        await table.update(entry.idempotencyKey, {
          status: online ? "failed" : "queued",
          error: cause instanceof Error ? cause.message : "Appointment sync failed.",
        });
        if (!online) break;
      }
    }
  })().finally(() => {
    activeSync = undefined;
  });

  return activeSync;
}
