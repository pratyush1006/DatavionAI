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
  Textarea,
} from "@/components/ui/textarea";

import type {
  Appointment,
  AppointmentFormValues,
} from "../domain";

import {
  useAppointmentsQuery,
  useCreateAppointmentMutation,
  useDeleteAppointmentMutation,
  useUpdateAppointmentMutation,
} from "../hooks";

/* =============================================================================
 * Defaults
 * =============================================================================
 */

const defaults: AppointmentFormValues = {
  organization: "",
  patient: "",
  provider: "",
  appointmentNumber: "",
  appointmentType: "consultation",
  status: "scheduled",
  priority: "normal",
  scheduledStart: "",
  scheduledEnd: "",
  durationMinutes: 30,
  reason: "",
  notes: "",
  isVirtual: false,
  meetingUrl: "",
  isActive: true,
};

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

/* =============================================================================
 * Appointment Form
 * =============================================================================
 */

type AppointmentFormProps = {
  readonly patient?: Appointment;

  readonly onClose: () => void;
};

function AppointmentForm({
  patient,
  onClose,
}: AppointmentFormProps) {
  const [
    values,
    setValues,
  ] =
    useState<AppointmentFormValues>(
      patient ?? defaults,
    );

  const createMutation =
    useCreateAppointmentMutation();

  const updateMutation =
    useUpdateAppointmentMutation();

  const mutation =
    patient
      ? updateMutation
      : createMutation;

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

  const handleSubmit = (
    event: React.FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    if (patient) {
      updateMutation.mutate(
        {
          id: patient.id,
          values,
        },
        {
          onSuccess: () => {
            toast.success(
              "Appointment updated.",
            );

            onClose();
          },

          onError: () => {
            toast.error(
              "Unable to save the appointment. Please verify all required identifiers and times.",
            );
          },
        },
      );

      return;
    }

    createMutation.mutate(
      values,
      {
        onSuccess: () => {
          toast.success(
            "Appointment scheduled.",
          );

          onClose();
        },

        onError: () => {
          toast.error(
            "Unable to save the appointment. Please verify all required identifiers and times.",
          );
        },
      },
    );
  };

  const textFields: Array<
    [
      keyof AppointmentFormValues,
      string,
      string?,
    ]
  > = [
    [
      "organization",
      "Organization UUID",
    ],
    [
      "patient",
      "Patient UUID",
    ],
    [
      "provider",
      "Provider UUID",
    ],
    [
      "appointmentNumber",
      "Appointment number",
    ],
    [
      "scheduledStart",
      "Start",
      "datetime-local",
    ],
    [
      "scheduledEnd",
      "End",
      "datetime-local",
    ],
    [
      "durationMinutes",
      "Duration (minutes)",
      "number",
    ],
    [
      "reason",
      "Reason",
    ],
  ];

  return (
    <form
      className="grid gap-4 md:grid-cols-2"
      onSubmit={handleSubmit}
    >
      {textFields.map(
        ([
          field,
          label,
          type,
        ]) => (
          <div key={field}>
            <Label htmlFor={field}>
              {label}
            </Label>

            <Input
              id={field}
              type={type}
              required={[
                "organization",
                "patient",
                "provider",
                "appointmentNumber",
                "scheduledStart",
                "scheduledEnd",
              ].includes(field)}
              value={String(
                values[field],
              )}
              onChange={(event) =>
                update(
                  field,
                  type === "number"
                    ? Number(
                        event.target.value,
                      )
                    : event.target.value,
                )
              }
            />
          </div>
        ),
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
          disabled={
            mutation.isPending
          }
        >
          {mutation.isPending
            ? "Saving..."
            : patient
              ? "Update appointment"
              : "Schedule appointment"}
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

  const {
    data = [],
    isPending,
  } =
    useAppointmentsQuery();

  const remove =
    useDeleteAppointmentMutation();

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
                          appointment.priority ===
                          "urgent"
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
                    </td>

                    <td className="p-4">
                      <div className="flex">
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
          patient={editing}
          onClose={() =>
            setOpen(false)
          }
        />
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
        description="This will permanently remove the appointment record."
        confirmLabel="Delete"
        confirmVariant="destructive"
        isLoading={
          remove.isPending
        }
        onConfirm={
          handleDelete
        }
      />
    </ListPage>
  );
}
