"use client";

import { useCallback, useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type { AppointmentFormValues } from "../domain";
import {
  enqueueOfflineAppointment,
  listOfflineAppointments,
  retryOfflineAppointment,
  synchronizeOfflineAppointments,
  updateOfflineAppointment,
  type OfflineAppointmentEntry,
} from "../offline/appointment-queue";
import { appointmentKeys } from "../api";

export function useOfflineAppointmentQueue() {
  const [entries, setEntries] = useState<OfflineAppointmentEntry[]>([]);
  const queryClient = useQueryClient();

  const refresh = useCallback(async () => {
    try {
      setEntries(await listOfflineAppointments());
    } catch {
      // IndexedDB can be unavailable in private browsing or storage-restricted contexts.
      setEntries([]);
    }
  }, []);

  const synchronize = useCallback(async () => {
    await synchronizeOfflineAppointments();
    await refresh();
    await queryClient.invalidateQueries({ queryKey: appointmentKeys.lists() });
  }, [queryClient, refresh]);

  const enqueue = useCallback(async (values: AppointmentFormValues) => {
    const entry = await enqueueOfflineAppointment(values);
    await refresh();
    return entry;
  }, [refresh]);

  const retry = useCallback(async (idempotencyKey: string) => {
    await retryOfflineAppointment(idempotencyKey);
    await synchronize();
  }, [synchronize]);

  const updateAppointment = useCallback(async (entry: OfflineAppointmentEntry, appointment: NonNullable<OfflineAppointmentEntry["appointment"]>) => {
    await updateOfflineAppointment(entry.idempotencyKey, appointment);
    await refresh();
  }, [refresh]);

  useEffect(() => {
    const startup = window.setTimeout(() => {
      void refresh();
      void synchronize();
    }, 0);
    const onOnline = () => void synchronize();
    window.addEventListener("online", onOnline);
    const timer = window.setInterval(() => void refresh(), 3000);
    return () => {
      window.clearTimeout(startup);
      window.removeEventListener("online", onOnline);
      window.clearInterval(timer);
    };
  }, [refresh, synchronize]);

  return { entries, enqueue, retry, synchronize, updateAppointment };
}
