"use client";

import {
  CalendarPlus,
  Pencil,
  Trash2,
  Video,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  toast,
} from "sonner";

import {
  LiveTranscriptionWorkspace,
} from "@/modules/transcription";

import {
  ConfirmDialog,
  EntityDialog,
} from "@/components/common/dialogs";

import {
  ListPage,
} from "@/components/common/page";

import {
  Badge,
} from "@/components/ui/badge";

import {
  Button,
} from "@/components/ui/button";

import {
  Input,
} from "@/components/ui/input";

import {
  Label,
} from "@/components/ui/label";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  Textarea,
} from "@/components/ui/textarea";

import type {
  Appointment,
  AppointmentFormValues,
} from "../domain";

import {
  APPOINTMENT_PRIORITIES,
  APPOINTMENT_TYPES,
} from "../domain";

import {
  createAppointmentDepositCheckout,
  verifyAppointmentDeposit,
} from "../api";

import {
  useAppointmentPatientsQuery,
  useAppointmentProvidersQuery,
  useAppointmentsQuery,
  useCheckInAppointmentMutation,
  useCreateAppointmentMutation,
  useDeleteAppointmentMutation,
  useNoShowAppointmentMutation,
  useOfflineAppointmentQueue,
  useRescheduleAppointmentMutation,
  useUpdateAppointmentMutation,
} from "../hooks";

/* =============================================================================
 * Defaults
 * =============================================================================
 */

function toDateTimeLocal(value: string | Date) {
  const date = value instanceof Date ? value : new Date(value);
  const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60_000);
  return localDate.toISOString().slice(0, 16);
}

function newAppointmentValues(): AppointmentFormValues {
  const start = new Date();
  start.setDate(start.getDate() + 1);
  start.setHours(9, 0, 0, 0);
  const end = new Date(start.getTime() + 30 * 60_000);

  return {
    patient: "",
    provider: "",
    appointmentNumber: `APPT-${Date.now()}`,
    appointmentType: "consultation",
    priority: "routine",
    scheduledStart: toDateTimeLocal(start),
    scheduledEnd: toDateTimeLocal(end),
    durationMinutes: 30,
    reason: "",
    notes: "",
    isVirtual: false,
    meetingUrl: "",
  };
}

function appointmentValues(appointment: Appointment): AppointmentFormValues {
  return {
    patient: appointment.patient,
    provider: appointment.provider,
    appointmentNumber: appointment.appointmentNumber,
    appointmentType: appointment.appointmentType,
    priority: appointment.priority,
    scheduledStart: toDateTimeLocal(appointment.scheduledStart),
    scheduledEnd: toDateTimeLocal(appointment.scheduledEnd),
    durationMinutes: appointment.durationMinutes,
    reason: appointment.reason,
    notes: appointment.notes,
    isVirtual: appointment.isVirtual,
    meetingUrl: appointment.meetingUrl,
  };
}

function isTomorrow(value: string): boolean {
  const appointmentDate = new Date(value);
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  return appointmentDate.getFullYear() === tomorrow.getFullYear() &&
    appointmentDate.getMonth() === tomorrow.getMonth() &&
    appointmentDate.getDate() === tomorrow.getDate();
}

/* =============================================================================
 * Formatting
 * =============================================================================
 */

function formatDate(
  value: string,
) {
  return new Intl.DateTimeFormat(
    "en-IN",
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(
    new Date(value),
  );
}

type RazorpayCallback = {
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
};

type RazorpayOptions = {
  key: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  order_id: string;
  handler: (response: RazorpayCallback) => void;
  modal: { ondismiss: () => void };
};

declare global {
  interface Window {
    Razorpay?: new (options: RazorpayOptions) => { open: () => void };
  }
}

async function loadRazorpay(): Promise<boolean> {
  if (window.Razorpay) return true;

  return new Promise((resolve) => {
    const existing = document.querySelector<HTMLScriptElement>(
      'script[src="https://checkout.razorpay.com/v1/checkout.js"]',
    );
    const script = existing ?? document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(Boolean(window.Razorpay));
    script.onerror = () => resolve(false);
    if (!existing) document.body.appendChild(script);
  });
}

async function openDepositCheckout(appointment: Appointment): Promise<Appointment | false> {
  const order = await createAppointmentDepositCheckout(appointment.id);
  if (!(await loadRazorpay()) || !window.Razorpay) {
    throw new Error("Unable to load the secure payment checkout.");
  }

  return new Promise((resolve, reject) => {
    const checkout = new window.Razorpay!({
      key: order.key_id,
      amount: order.amount,
      currency: order.currency,
      name: "DatavionOS",
      description: `Appointment deposit · ₹${appointment.depositAmount.toFixed(2)}`,
      order_id: order.order_id,
      handler: (response) => {
        void verifyAppointmentDeposit({ appointmentId: appointment.id, response })
          .then(resolve)
          .catch(reject);
      },
      modal: { ondismiss: () => resolve(false) },
    });
    checkout.open();
  });
}

/* =============================================================================
 * Appointment Form
 * =============================================================================
 */

type AppointmentFormProps = {
  readonly appointment?: Appointment;

  readonly onClose: () => void;

  readonly onBooked: (trackingToken: string) => void;

  readonly onQueueOffline: (values: AppointmentFormValues) => Promise<void>;
};

function AppointmentForm({
  appointment,
  onClose,
  onBooked,
  onQueueOffline,
}: AppointmentFormProps) {
  const [values, setValues] = useState<AppointmentFormValues>(
    appointment ? appointmentValues(appointment) : newAppointmentValues(),
  );
  const [pendingPaymentAppointment, setPendingPaymentAppointment] = useState<Appointment>();
  const [isCheckoutPending, setIsCheckoutPending] = useState(false);

  const patientsQuery = useAppointmentPatientsQuery();
  const providersQuery = useAppointmentProvidersQuery();

  const createMutation =
    useCreateAppointmentMutation();

  const updateMutation =
    useUpdateAppointmentMutation();

  const rescheduleMutation = useRescheduleAppointmentMutation();
  const isSaving = createMutation.isPending || updateMutation.isPending || rescheduleMutation.isPending || isCheckoutPending;

  const update = (
    field: keyof AppointmentFormValues,
    value:
      | string
      | number
      | boolean,
  ) => {
    setValues(
      (current) => ({
        ...current,
        [field]: value,
      }),
    );
  };

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (!values.patient || !values.provider) {
      toast.error("Select a patient and provider before scheduling.");
      return;
    }

    try {
      if (appointment) {
        const previousValues = appointmentValues(appointment);
        const scheduleChanged =
          values.scheduledStart !== previousValues.scheduledStart ||
          values.scheduledEnd !== previousValues.scheduledEnd ||
          values.durationMinutes !== previousValues.durationMinutes;

        if (scheduleChanged) {
          if (!appointment.canReschedule) {
            toast.error("This appointment can no longer be rescheduled.");
            return;
          }
          if (!isTomorrow(values.scheduledStart)) {
            toast.error("Appointments can only be rescheduled to tomorrow.");
            return;
          }
          await rescheduleMutation.mutateAsync({
            id: appointment.id,
            values: {
              scheduledStart: values.scheduledStart,
              scheduledEnd: values.scheduledEnd,
              durationMinutes: values.durationMinutes,
            },
          });
        }

        await updateMutation.mutateAsync({
          id: appointment.id,
          values,
        });

        toast.success("Appointment updated.");
      } else {
        if (!navigator.onLine) {
          await onQueueOffline(values);
          toast.success("Appointment saved offline. It will sync automatically when you reconnect.");
          onClose();
          return;
        }

        const booking = pendingPaymentAppointment ?? await createMutation.mutateAsync(values);
        setPendingPaymentAppointment(booking);
        setIsCheckoutPending(true);
        const paid = await openDepositCheckout(booking);
        if (!paid) {
          toast.info("Your appointment is reserved. Complete the deposit payment to finish booking.");
          return;
        }
        setPendingPaymentAppointment(undefined);
        if (booking.trackingToken) onBooked(booking.trackingToken);
        toast.success("Deposit paid and appointment scheduled.");
      }

      onClose();
    } catch (error) {
      toast.error(
        error instanceof Error
          ? error.message
          : "Unable to save the appointment. Check the selected records and times.",
      );
    } finally {
      setIsCheckoutPending(false);
    }
  };

  return (
    <form
      className="grid gap-4 md:grid-cols-2"
      onSubmit={handleSubmit}
    >
      <div>
        <Label htmlFor="patient">Patient</Label>
        <Select
          value={values.patient}
          onValueChange={(value) => update("patient", value)}
          disabled={Boolean(appointment) || (patientsQuery.isPending && !patientsQuery.data)}
        >
          <SelectTrigger id="patient">
            <SelectValue placeholder={patientsQuery.isPending ? "Loading patients..." : "Choose a patient"} />
          </SelectTrigger>
          <SelectContent>
            {(patientsQuery.data ?? []).map((option) => (
              <SelectItem key={option.id} value={option.id}>{option.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="provider">Provider</Label>
        <Select
          value={values.provider}
          onValueChange={(value) => update("provider", value)}
          disabled={Boolean(appointment) || (providersQuery.isPending && !providersQuery.data)}
        >
          <SelectTrigger id="provider">
            <SelectValue placeholder={providersQuery.isPending ? "Loading providers..." : "Choose a provider"} />
          </SelectTrigger>
          <SelectContent>
            {(providersQuery.data ?? []).map((option) => (
              <SelectItem key={option.id} value={option.id}>{option.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="appointmentNumber">Appointment number</Label>
        <Input
          id="appointmentNumber"
          required
          value={values.appointmentNumber}
          onChange={(event) => update("appointmentNumber", event.target.value)}
        />
      </div>

      <div>
        <Label htmlFor="appointmentType">Appointment type</Label>
        <Select
          value={values.appointmentType}
          onValueChange={(value) => update("appointmentType", value as AppointmentFormValues["appointmentType"])}
        >
          <SelectTrigger id="appointmentType"><SelectValue /></SelectTrigger>
          <SelectContent>
            {APPOINTMENT_TYPES.map((type) => (
              <SelectItem key={type} value={type}>{type.replaceAll("_", " ")}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="priority">Priority</Label>
        <Select
          value={values.priority}
          onValueChange={(value) => update("priority", value as AppointmentFormValues["priority"])}
        >
          <SelectTrigger id="priority"><SelectValue /></SelectTrigger>
          <SelectContent>
            {APPOINTMENT_PRIORITIES.map((priority) => (
              <SelectItem key={priority} value={priority}>{priority}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="scheduledStart">Start</Label>
        <Input
          id="scheduledStart"
          type="datetime-local"
          required
          disabled={appointment !== undefined && !appointment.canReschedule}
          value={values.scheduledStart}
          onChange={(event) => update("scheduledStart", event.target.value)}
        />
      </div>

      <div>
        <Label htmlFor="scheduledEnd">End</Label>
        <Input
          id="scheduledEnd"
          type="datetime-local"
          required
          disabled={appointment !== undefined && !appointment.canReschedule}
          value={values.scheduledEnd}
          onChange={(event) => update("scheduledEnd", event.target.value)}
        />
      </div>

      <div>
        <Label htmlFor="durationMinutes">Duration (minutes)</Label>
        <Input
          id="durationMinutes"
          type="number"
          min={1}
          required
          value={values.durationMinutes}
          onChange={(event) => update("durationMinutes", Number(event.target.value))}
        />
      </div>

      <div>
        <Label htmlFor="reason">Reason</Label>
        <Input
          id="reason"
          value={values.reason}
          onChange={(event) => update("reason", event.target.value)}
        />
      </div>

      {((patientsQuery.isError && !patientsQuery.data) || (providersQuery.isError && !providersQuery.data)) && (
        <p className="md:col-span-2 text-sm text-destructive">
          No cached patient/provider list is available. Connect once to load records before booking offline.
        </p>
      )}

      {pendingPaymentAppointment && (
        <p className="md:col-span-2 text-sm text-muted-foreground">
          Appointment reserved. Pay the non-refundable 50% deposit of ₹{pendingPaymentAppointment.depositAmount.toFixed(2)} to complete booking.
        </p>
      )}

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={
            values.isVirtual
          }
          onChange={(event) =>
            update(
              "isVirtual",
              event.target.checked,
            )
          }
        />

        Virtual appointment
      </label>

      <div>
        <Label htmlFor="meetingUrl">
          Meeting URL
        </Label>

        <Input
          id="meetingUrl"
          type="url"
          required={values.isVirtual}
          value={
            values.meetingUrl
          }
          onChange={(event) =>
            update(
              "meetingUrl",
              event.target.value,
            )
          }
        />
      </div>

      <div className="md:col-span-2">
        <Label htmlFor="notes">
          Clinical scheduling notes
        </Label>

        <Textarea
          id="notes"
          value={
            values.notes
          }
          onChange={(event) =>
            update(
              "notes",
              event.target.value,
            )
          }
        />
      </div>

      <div className="md:col-span-2 flex justify-end gap-3">
        <Button
          type="button"
          variant="outline"
          onClick={onClose}
        >
          Cancel
        </Button>

        <Button
          type="submit"
          disabled={isSaving || (!patientsQuery.data && patientsQuery.isError) || (!providersQuery.data && providersQuery.isError)}
        >
          {isSaving
            ? "Saving..."
            : appointment
              ? "Update appointment"
              : pendingPaymentAppointment
                ? "Pay deposit"
                : "Pay deposit & schedule"}
        </Button>
      </div>
    </form>
  );
}

/* =============================================================================
 * Page
 * =============================================================================
 */

export function AppointmentsPage() {
  const [
    open,
    setOpen,
  ] =
    useState(false);

  const [
    editing,
    setEditing,
  ] =
    useState<
      Appointment | undefined
    >();

  const [
    deleting,
    setDeleting,
  ] =
    useState<
      Appointment | undefined
    >();
  const [noShowSelection, setNoShowSelection] = useState<Appointment>();

  const [checkInSelection, setCheckInSelection] = useState<Appointment>();
  const [recordingConsent, setRecordingConsent] = useState(false);
  const [scribeSessionId, setScribeSessionId] = useState<string>();
  const [latestTrackingUrl, setLatestTrackingUrl] = useState<string>();

  const {
    data = [],
    isPending,
    isError,
    refetch,
  } =
    useAppointmentsQuery();

  const remove =
    useDeleteAppointmentMutation();

  const checkInMutation = useCheckInAppointmentMutation();
  const noShowMutation = useNoShowAppointmentMutation();
  const offlineQueue = useOfflineAppointmentQueue();

  const handleCheckIn = async (consent: boolean) => {
    if (!checkInSelection) return;
    try {
      const result = await checkInMutation.mutateAsync({
        appointmentId: checkInSelection.id,
        recordingConsent: consent,
      });
      setCheckInSelection(undefined);
      setRecordingConsent(false);
      if (result.transcription_session) {
        setScribeSessionId(result.transcription_session.session_id);
        toast.success("Patient checked in. Starting the AI scribe.");
      } else {
        toast.success("Patient checked in without recording.");
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Unable to check in patient.");
    }
  };

  const handleCreate = () => {
    setEditing(undefined);
    setOpen(true);
  };

  const handleEdit = (
    appointment: Appointment,
  ) => {
    setEditing(appointment);
    setOpen(true);
  };

  const handleDelete = () => {
    if (!deleting) {
      return;
    }

    remove.mutate(
      deleting.id,
      {
        onSuccess: () => {
          toast.success(
            "Appointment deleted.",
          );

          setDeleting(
            undefined,
          );
        },

        onError: () => {
          toast.error(
            "Unable to delete appointment.",
          );
        },
      },
    );
  };

  const handleNoShow = () => {
    if (!noShowSelection) return;
    noShowMutation.mutate(noShowSelection.id, {
      onSuccess: () => {
        toast.success("Appointment marked as no-show. The booking deposit was not refunded.");
        setNoShowSelection(undefined);
      },
      onError: () => toast.error("Unable to mark this appointment as no-show."),
    });
  };

  const handleQueuedPayment = async (entry: (typeof offlineQueue.entries)[number]) => {
    if (!entry.appointment) return;
    try {
      const paidAppointment = await openDepositCheckout(entry.appointment);
      if (paidAppointment) {
        await offlineQueue.updateAppointment(entry, paidAppointment);
        toast.success("Offline appointment synced and deposit paid.");
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Unable to collect the appointment deposit.");
    }
  };

  return (
    <ListPage
      title="Appointments"
      description="Schedule and manage patient care visits across in-person and virtual settings."
      actions={
        <Button
          onClick={handleCreate}
        >
          <CalendarPlus className="mr-2 h-4 w-4" />

          Schedule appointment
        </Button>
      }
    >
      {latestTrackingUrl && (
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-lg border bg-card p-4 text-sm">
          <div>
            <p className="font-medium">Patient status tracking link</p>
            <a className="break-all text-primary underline" href={latestTrackingUrl} target="_blank" rel="noreferrer">
              {latestTrackingUrl}
            </a>
          </div>
          <Button
            variant="outline"
            onClick={() => void navigator.clipboard.writeText(latestTrackingUrl).then(() => toast.success("Tracking link copied."))}
          >
            Copy link
          </Button>
        </div>
      )}
      {offlineQueue.entries.length > 0 && (
        <section className="mb-4 space-y-3 rounded-lg border bg-card p-4" aria-label="Offline appointment synchronization">
          <div>
            <h2 className="font-medium">Offline appointments</h2>
            <p className="text-sm text-muted-foreground">
              Queued bookings sync automatically when this device reconnects. Free-text notes are not stored offline. Complete payment after sync.
            </p>
          </div>
          {offlineQueue.entries.map((entry) => (
            <div key={entry.idempotencyKey} className="flex flex-wrap items-center justify-between gap-3 border-t pt-3 text-sm">
              <div>
                <p className="font-medium">{entry.values.appointmentNumber}</p>
                <p className="text-muted-foreground">
                  {entry.status === "queued" ? "Waiting to sync" : entry.status === "syncing" ? "Syncing…" : entry.status === "failed" ? `Sync failed: ${entry.error}` : entry.appointment?.depositPaid ? "Synced · deposit paid" : "Synced · deposit payment required"}
                </p>
                {entry.appointment?.trackingToken && (
                  <a className="text-primary underline" href={`/appointments/track/${encodeURIComponent(entry.appointment.trackingToken)}`}>
                    Patient tracking link
                  </a>
                )}
              </div>
              {entry.status === "failed" && (
                <Button variant="outline" size="sm" onClick={() => void offlineQueue.retry(entry.idempotencyKey)}>Retry sync</Button>
              )}
              {entry.status === "synced" && entry.appointment && !entry.appointment.depositPaid && (
                <Button size="sm" onClick={() => void handleQueuedPayment(entry)}>Pay 50% deposit</Button>
              )}
            </div>
          ))}
        </section>
      )}
      <div className="overflow-hidden rounded-lg border">
        <table className="w-full text-sm">
          <thead className="bg-muted/50 text-left">
            <tr>
              <th className="p-4">
                Appointment
              </th>

              <th className="p-4">
                Scheduled
              </th>

              <th className="p-4">
                Priority
              </th>

              <th className="p-4">
                Status
              </th>

              <th className="p-4" />
            </tr>
          </thead>

          <tbody>
            {isPending ? (
              <tr>
                <td
                  className="p-8 text-center"
                  colSpan={5}
                >
                  Loading appointments...
                </td>
              </tr>
            ) : isError ? (
              <tr>
                <td className="p-8 text-center text-destructive" colSpan={5}>
                  Could not load appointments. <Button variant="link" onClick={() => void refetch()}>Retry</Button>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td
                  className="p-8 text-center text-muted-foreground"
                  colSpan={5}
                >
                  No appointments scheduled.
                </td>
              </tr>
            ) : (
              data.map(
                (
                  appointment,
                ) => (
                  <tr
                    key={
                      appointment.id
                    }
                    className="border-t"
                  >
                    <td className="p-4">
                      <div className="font-medium">
                        {
                          appointment.appointmentNumber
                        }
                      </div>

                      <div className="text-xs text-muted-foreground">
                        {appointment.appointmentType.replaceAll(
                          "_",
                          " ",
                        )}

                        {appointment.isVirtual && (
                          <Video className="ml-2 inline h-3 w-3" />
                        )}
                      </div>
                    </td>

                    <td className="p-4">
                      {formatDate(
                        appointment.scheduledStart,
                      )}
                    </td>

                    <td className="p-4">
                      <Badge
                        variant={
                          appointment.priority === "urgent" || appointment.priority === "emergency"
                            ? "destructive"
                            : "secondary"
                        }
                      >
                        {
                          appointment.priority
                        }
                      </Badge>
                    </td>

                    <td className="p-4">
                      <Badge>
                        {appointment.status.replaceAll(
                          "_",
                          " ",
                        )}
                      </Badge>
                      <div className="mt-1 text-xs text-muted-foreground">
                        Deposit {appointment.depositPaid ? "paid" : "due"}
                      </div>
                    </td>

                    <td className="p-4">
                      <div className="flex">
                        {(appointment.status === "scheduled" || appointment.status === "confirmed") && (
                          <Button
                            variant="outline"
                            size="sm"
                            disabled={!appointment.depositPaid || checkInMutation.isPending}
                            onClick={() => {
                              setRecordingConsent(false);
                              setCheckInSelection(appointment);
                            }}
                          >
                            Check in
                          </Button>
                        )}
                        {(appointment.status === "scheduled" || appointment.status === "confirmed") &&
                          new Date(appointment.scheduledEnd) <= new Date() && (
                            <Button
                              variant="outline"
                              size="sm"
                              disabled={noShowMutation.isPending}
                              onClick={() => setNoShowSelection(appointment)}
                            >
                              Mark no-show
                            </Button>
                          )}
                        <Button
                          variant="ghost"
                          size="icon-sm"
                          onClick={() =>
                            handleEdit(
                              appointment,
                            )
                          }
                        >
                          <Pencil className="h-4 w-4" />

                          <span className="sr-only">
                            Edit appointment
                          </span>
                        </Button>

                        <Button
                          variant="ghost"
                          size="icon-sm"
                          onClick={() =>
                            setDeleting(
                              appointment,
                            )
                          }
                        >
                          <Trash2 className="h-4 w-4 text-destructive" />

                          <span className="sr-only">
                            Delete appointment
                          </span>
                        </Button>
                      </div>
                    </td>
                  </tr>
                ),
              )
            )}
          </tbody>
        </table>
      </div>

      <EntityDialog
        open={open}
        onOpenChange={
          setOpen
        }
        title={
          editing
            ? "Edit appointment"
            : "Schedule appointment"
        }
        description="Appointments are recorded against the selected organization, patient, and provider."
        size="xl"
      >
        <AppointmentForm
          key={editing?.id ?? "new-appointment"}
          appointment={editing}
          onBooked={(token) => setLatestTrackingUrl(
            `${window.location.origin}/appointments/track/${encodeURIComponent(token)}`,
          )}
          onQueueOffline={async (values) => {
            await offlineQueue.enqueue(values);
          }}
          onClose={() =>
            setOpen(false)
          }
        />
      </EntityDialog>

      <EntityDialog
        open={Boolean(checkInSelection)}
        onOpenChange={(value) => {
          if (!value) {
            setCheckInSelection(undefined);
            setRecordingConsent(false);
          }
        }}
        title="Patient check-in and AI scribe"
        description="Ask the patient for consent before recording. Recording is optional; declining will not block check-in."
        size="md"
      >
        <div className="space-y-5">
          <label className="flex items-start gap-3 text-sm">
            <input
              type="checkbox"
              checked={recordingConsent}
              onChange={(event) => setRecordingConsent(event.target.checked)}
            />
            <span>
              The patient consents to audio recording and AI transcription for this visit. The microphone will start after check-in.
            </span>
          </label>
          <div className="flex justify-end gap-3">
            <Button variant="outline" disabled={checkInMutation.isPending} onClick={() => void handleCheckIn(false)}>
              Check in without recording
            </Button>
            <Button disabled={!recordingConsent || checkInMutation.isPending} onClick={() => void handleCheckIn(true)}>
              {checkInMutation.isPending ? "Checking in..." : "Check in & start scribe"}
            </Button>
          </div>
        </div>
      </EntityDialog>

      <EntityDialog
        open={Boolean(scribeSessionId)}
        onOpenChange={(value) => {
          if (!value) {
            setScribeSessionId(undefined);
          }
        }}
        title="Clinical visit · AI scribe"
        description="Live transcription is a draft aid; the doctor must review all notes and prescriptions."
        size="lg"
      >
        {scribeSessionId && (
          <LiveTranscriptionWorkspace
            key={scribeSessionId}
            sessionId={scribeSessionId}
            autoStart
          />
        )}
      </EntityDialog>

      <ConfirmDialog
        open={Boolean(
          deleting,
        )}
        onOpenChange={(
          value,
        ) =>
          !value &&
          setDeleting(
            undefined,
          )
        }
        title="Delete appointment"
        description="This will remove the appointment from active records."
        confirmLabel="Delete"
        confirmVariant="destructive"
        isLoading={
          remove.isPending
        }
        onConfirm={
          handleDelete
        }
      />

      <ConfirmDialog
        open={Boolean(noShowSelection)}
        onOpenChange={(value) => !value && setNoShowSelection(undefined)}
        title="Mark appointment as no-show?"
        description="This can only be recorded after the scheduled end time. The 50% booking deposit remains non-refundable."
        confirmLabel="Mark no-show"
        confirmVariant="destructive"
        isLoading={noShowMutation.isPending}
        onConfirm={handleNoShow}
      />
    </ListPage>
  );
}
