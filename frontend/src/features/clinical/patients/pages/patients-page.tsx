"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Pencil, Plus, Search, Trash2, Users } from "lucide-react";
import { useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { ConfirmDialog, EntityDialog } from "@/components/common/dialogs";
import { ListPage } from "@/components/common/page";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

import { createPatient, deletePatient, fetchPatients, updatePatient } from "../api/patients";
import { PATIENT_GENDERS, PATIENT_STATUSES, type Patient, type PatientFormValues } from "../domain";

const schema = z.object({
  organization: z.string().uuid("Enter the organization UUID."), mrn: z.string().trim().min(1, "MRN is required."),
  firstName: z.string().trim().min(1, "First name is required."), middleName: z.string(), lastName: z.string().trim().min(1, "Last name is required."),
  preferredName: z.string(), dateOfBirth: z.string().min(1, "Date of birth is required."),
  gender: z.enum(PATIENT_GENDERS), maritalStatus: z.string(), bloodGroup: z.string(), phone: z.string(), email: z.string().email("Enter a valid email.").or(z.literal("")),
  address: z.string(), city: z.string(), state: z.string(), country: z.string().min(1), postalCode: z.string(), status: z.enum(PATIENT_STATUSES), isActive: z.boolean(),
});

const defaults: PatientFormValues = { organization: "", mrn: "", firstName: "", middleName: "", lastName: "", preferredName: "", dateOfBirth: "", gender: "UNKNOWN", maritalStatus: "", bloodGroup: "", phone: "", email: "", address: "", city: "", state: "", country: "India", postalCode: "", status: "ACTIVE", isActive: true };

function valuesFor(patient?: Patient): PatientFormValues { return patient ? { organization: patient.organization, mrn: patient.mrn, firstName: patient.firstName, middleName: patient.middleName, lastName: patient.lastName, preferredName: patient.preferredName, dateOfBirth: patient.dateOfBirth, gender: patient.gender, maritalStatus: patient.maritalStatus, bloodGroup: patient.bloodGroup, phone: patient.phone, email: patient.email, address: patient.address, city: patient.city, state: patient.state, country: patient.country, postalCode: patient.postalCode, status: patient.status, isActive: patient.isActive } : defaults; }

function PatientForm({ patient, onClose }: { patient?: Patient; onClose: () => void }) {
  const queryClient = useQueryClient();
  const form = useForm<PatientFormValues>({ resolver: zodResolver(schema), defaultValues: valuesFor(patient) });
  const mutation = useMutation({ mutationFn: (values: PatientFormValues) => patient ? updatePatient({ id: patient.id, values }) : createPatient(values), onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["patients"] }); toast.success(patient ? "Patient updated." : "Patient created."); onClose(); }, onError: () => toast.error("Unable to save patient. Check the entered details.") });
  const fields: Array<[keyof PatientFormValues, string, string?]> = [["organization", "Organization UUID"], ["mrn", "Medical record number"], ["firstName", "First name"], ["middleName", "Middle name"], ["lastName", "Last name"], ["preferredName", "Preferred name"], ["dateOfBirth", "Date of birth", "date"], ["phone", "Phone"], ["email", "Email", "email"], ["address", "Address"], ["city", "City"], ["state", "State"], ["country", "Country"], ["postalCode", "Postal code"]];
  return <form className="grid gap-4 md:grid-cols-2" onSubmit={form.handleSubmit((values) => mutation.mutate(values))}>{fields.map(([name, label, type]) => <div key={name} className={name === "address" ? "md:col-span-2" : ""}><Label htmlFor={name}>{label}</Label><Input id={name} type={type} {...form.register(name)} /><p className="mt-1 text-xs text-destructive">{form.formState.errors[name]?.message}</p></div>)}<Select value={form.watch("gender")} onValueChange={(value) => form.setValue("gender", value as Patient["gender"])}><SelectTrigger><SelectValue placeholder="Gender" /></SelectTrigger><SelectContent>{PATIENT_GENDERS.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}</SelectContent></Select><Select value={form.watch("status")} onValueChange={(value) => form.setValue("status", value as Patient["status"])}><SelectTrigger><SelectValue placeholder="Status" /></SelectTrigger><SelectContent>{PATIENT_STATUSES.map((option) => <SelectItem key={option} value={option}>{option}</SelectItem>)}</SelectContent></Select><div className="md:col-span-2 flex justify-end gap-3"><Button type="button" variant="outline" onClick={onClose}>Cancel</Button><Button type="submit" disabled={mutation.isPending}>{mutation.isPending ? "Saving..." : patient ? "Update Patient" : "Create Patient"}</Button></div></form>;
}

export function PatientsPage() {
  const [search, setSearch] = useState(""); const [editing, setEditing] = useState<Patient | undefined>(); const [formOpen, setFormOpen] = useState(false); const [deleting, setDeleting] = useState<Patient | undefined>(); const queryClient = useQueryClient();
  const { data = [], isPending } = useQuery({ queryKey: ["patients"], queryFn: fetchPatients }); const remove = useMutation({ mutationFn: deletePatient, onSuccess: () => { queryClient.invalidateQueries({ queryKey: ["patients"] }); toast.success("Patient deleted."); setDeleting(undefined); }, onError: () => toast.error("Unable to delete patient.") });
  const patients = useMemo(() => data.filter((patient) => `${patient.displayName} ${patient.mrn} ${patient.phone}`.toLowerCase().includes(search.toLowerCase())), [data, search]);
  return <ListPage title="Patients" description="Manage patient demographics and clinical registration records." actions={<Button onClick={() => { setEditing(undefined); setFormOpen(true); }}><Plus className="mr-2 h-4 w-4" />New Patient</Button>}><div className="relative mb-6 max-w-md"><Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" /><Input className="pl-9" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search name, MRN, or phone" /></div><div className="overflow-hidden rounded-lg border"><table className="w-full text-sm"><thead className="bg-muted/50 text-left"><tr><th className="p-4">Patient</th><th className="p-4">MRN</th><th className="p-4">Demographics</th><th className="p-4">Contact</th><th className="p-4">Status</th><th className="p-4" /></tr></thead><tbody>{isPending ? <tr><td className="p-8 text-center" colSpan={6}>Loading patients...</td></tr> : patients.length === 0 ? <tr><td className="p-8 text-center text-muted-foreground" colSpan={6}>No patients found.</td></tr> : patients.map((patient) => <tr key={patient.id} className="border-t"><td className="p-4"><div className="flex items-center gap-3"><div className="rounded-full bg-primary/10 p-2"><Users className="h-4 w-4 text-primary" /></div><div><div className="font-medium">{patient.displayName}</div><div className="text-xs text-muted-foreground">{patient.age} years · {patient.gender}</div></div></div></td><td className="p-4 font-mono text-xs">{patient.mrn}</td><td className="p-4">{patient.dateOfBirth}</td><td className="p-4">{patient.phone || patient.email || "—"}</td><td className="p-4"><Badge variant={patient.isActive ? "default" : "secondary"}>{patient.status}</Badge></td><td className="p-4"><div className="flex"><Button variant="ghost" size="icon-sm" onClick={() => { setEditing(patient); setFormOpen(true); }}><Pencil className="h-4 w-4" /><span className="sr-only">Edit patient</span></Button><Button variant="ghost" size="icon-sm" onClick={() => setDeleting(patient)}><Trash2 className="h-4 w-4 text-destructive" /><span className="sr-only">Delete patient</span></Button></div></td></tr>)}</tbody></table></div><EntityDialog open={formOpen} onOpenChange={setFormOpen} title={editing ? "Edit Patient" : "New Patient"} description="Maintain the patient demographic and contact record." size="xl"><PatientForm patient={editing} onClose={() => setFormOpen(false)} /></EntityDialog><ConfirmDialog open={Boolean(deleting)} onOpenChange={(open) => !open && setDeleting(undefined)} title="Delete Patient" description={<>Delete <strong>{deleting?.displayName}</strong>? This action cannot be undone.</>} confirmLabel="Delete" confirmVariant="destructive" isLoading={remove.isPending} onConfirm={() => deleting && remove.mutate(deleting.id)} /></ListPage>;
}
