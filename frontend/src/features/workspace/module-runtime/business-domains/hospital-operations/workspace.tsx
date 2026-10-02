"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { apiClient } from "@/core/api";
import { authRuntime } from "@/core/auth";
import { useBootstrap } from "@/core/bootstrap";
import { patientEndpoints } from "@/features/clinical/patients/api/endpoints";
import type { ModuleRuntimeDefinition } from "../../domain/types";
import { ModuleDataTable } from "../../data/module-data-table";
import type { HospitalOperationsRuntimeContract } from "./types";

export type HospitalOperationsBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const hospitalOperationsRuntimeContract: HospitalOperationsRuntimeContract = {
  department: "hospital_operations",
  authorizationAuthority: "backend_effective_context",
  dataAdapter: "listModule",
};

type Facility = { uuid: string; name: string; code: string };
type Unit = { uuid: string; facility: string; name: string; code: string };
type Room = { uuid: string; facility: string; unit: string; number: string };
type CatalogOption = { id: string; name: string; code: string };
type CapacityCatalog = { facilities: readonly CatalogOption[]; units: readonly CatalogOption[]; rooms: readonly CatalogOption[]; beds: readonly CatalogOption[] };
type AdmissionUnit = { uuid: string; name: string; active: boolean };
type AdmissionRoom = { uuid: string; unit: string; number: string };
type AdmissionBed = { uuid: string; room: string; label: string; status: string };
type AdmissionPatient = { id: string; label: string };

type ApiCollection<T> = readonly T[] | Readonly<{ results?: readonly T[]; data?: readonly T[] }>;

function messageFrom(error: unknown): string {
  const responseData = (error as { response?: { data?: unknown } })?.response?.data;
  if (typeof responseData === "object" && responseData !== null) {
    const details = Object.entries(responseData as Record<string, unknown>)
      .map(([field, value]) => `${field === "detail" ? "" : `${field}: `}${Array.isArray(value) ? value.join(", ") : String(value)}`)
      .join(" ")
      .trim();
    if (details) return details;
  }
  return error instanceof Error ? error.message : "The setup request could not be completed.";
}

/**
 * Django REST Framework list endpoints may be paginated or may return a bare
 * array when pagination is disabled. Keep the UI compatible with both API
 * contracts so an otherwise successful setup request cannot crash the route.
 */
function collectionRows<T>(payload: ApiCollection<T>): T[] {
  if (Array.isArray(payload)) return [...payload];
  const paginated = payload as Readonly<{ results?: readonly T[]; data?: readonly T[] }>;
  if (Array.isArray(paginated.results)) return [...paginated.results];
  if (Array.isArray(paginated.data)) return [...paginated.data];
  return [];
}

function CapacitySetup() {
  const { bootstrap, isError: isBootstrapError, error: bootstrapError } = useBootstrap();
  const tenantId = bootstrap?.tenant?.id;
  const organizationId = bootstrap?.organization?.id;
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [units, setUnits] = useState<Unit[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [catalog, setCatalog] = useState<CapacityCatalog>({ facilities: [], units: [], rooms: [], beds: [] });
  const [facilityId, setFacilityId] = useState("");
  const [unitId, setUnitId] = useState("");
  const [roomId, setRoomId] = useState("");
  const [facilityName, setFacilityName] = useState("");
  const [facilityCode, setFacilityCode] = useState("");
  const [unitName, setUnitName] = useState("");
  const [unitCode, setUnitCode] = useState("");
  const [roomNumber, setRoomNumber] = useState("");
  const [bedLabel, setBedLabel] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const bootstrapContextError = !bootstrap && isBootstrapError
    ? bootstrapError?.message ?? "Unable to load tenant context."
    : bootstrap && (!tenantId || !organizationId)
      ? "Tenant and organization context required. Select an active workspace and organization."
      : null;

  const reload = useCallback(async () => {
    if (!tenantId || !organizationId) return;

    const user = authRuntime.userStorage.updateUser({ tenantId, organizationId });
    if (!user) {
      setError("Authenticated user context is unavailable. Please sign in again.");
      return;
    }

    try {
      const [facilityResponse, unitResponse, roomResponse, catalogResponse] = await Promise.all([
        apiClient.axios.get<ApiCollection<Facility>>("/hospital-operations/facilities/"),
        apiClient.axios.get<ApiCollection<Unit>>("/hospital-operations/units/"),
        apiClient.axios.get<ApiCollection<Room>>("/hospital-operations/rooms/setup/"),
        apiClient.axios.get<CapacityCatalog>("/hospital-operations/capacity-catalog/"),
      ]);
      setFacilities(collectionRows(facilityResponse.data));
      setUnits(collectionRows(unitResponse.data));
      setRooms(collectionRows(roomResponse.data));
      setCatalog(catalogResponse.data);
    } catch (loadError) {
      setError(messageFrom(loadError));
    }
  }, [tenantId, organizationId]);

  useEffect(() => {
    if (tenantId && organizationId) {
      void Promise.resolve().then(reload);
    }
  }, [organizationId, reload, tenantId]);

  const scopedUnits = useMemo(
    () => units.filter((unit) => unit.facility === facilityId),
    [facilityId, units],
  );
  const scopedRooms = useMemo(
    () => rooms.filter((room) => room.unit === unitId),
    [rooms, unitId],
  );

  async function submit(action: () => Promise<void>) {
    setSaving(true);
    setError(null);
    setNotice(null);
    try {
      await action();
      await reload();
    } catch (submitError) {
      setError(messageFrom(submitError));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="card border-0 shadow-sm" aria-label="Hospital capacity setup">
      <div className="card-body p-4">
        <div className="d-flex flex-column flex-lg-row align-items-lg-start justify-content-between gap-2 mb-4">
          <div>
            <div className="text-primary small text-uppercase fw-semibold mb-1">Capacity configuration</div>
            <h2 className="h4 mb-1">Build your care-location hierarchy</h2>
            <p className="text-body-secondary mb-0">Set up a facility, then its wards, rooms, and beds. Each selection is restricted to the active organization.</p>
          </div>
          <span className="badge rounded-pill text-bg-light border px-3 py-2">Facility → Ward → Room → Bed</span>
        </div>
        <div className="alert alert-light border d-flex gap-2 align-items-start py-2 px-3 mb-4" role="note">
          <span className="fw-semibold">Start here:</span>
          <span className="text-body-secondary">Create the facility first. The next step becomes available after it has been saved.</span>
        </div>
        {bootstrapContextError || error ? <div className="alert alert-danger" role="alert">{bootstrapContextError ?? error}</div> : null}
        {notice ? <div className="alert alert-success" role="status">{notice}</div> : null}
        <div className="row g-3">
          <form className="col-12 col-md-6 col-xl-3" onSubmit={(event) => { event.preventDefault(); void submit(async () => {
            const response = await apiClient.axios.post<Facility>("/hospital-operations/facilities/", { name: facilityName, code: facilityCode });
            setFacilityId(response.data.uuid); setFacilityName(""); setFacilityCode(""); setNotice("Facility created. Continue with a ward.");
          }); }}>
            <div className="border rounded-3 p-3"><div className="d-flex align-items-center gap-2 mb-3"><span className="badge rounded-pill text-bg-primary">1</span><h3 className="h6 mb-0">Facility</h3></div>
              <label className="form-label small" htmlFor="facility-template">Facility</label><select id="facility-template" className="form-select mb-3" required value={facilityCode} onChange={(event) => { const option = catalog.facilities.find((item) => item.code === event.target.value); setFacilityName(option?.name ?? ""); setFacilityCode(option?.code ?? ""); }}><option value="">Choose facility</option>{catalog.facilities.map((item) => { const exists = facilities.some((facility) => facility.code === item.code); return <option key={item.id} value={item.code} disabled={exists}>{item.name} ({item.code}){exists ? " — already configured" : ""}</option>; })}</select>
              <button className="btn btn-primary w-100" disabled={saving}>Create facility</button>
            </div>
          </form>
          <form className="col-12 col-md-6 col-xl-3" onSubmit={(event) => { event.preventDefault(); void submit(async () => {
            const response = await apiClient.axios.post<Unit>("/hospital-operations/units/", { facility: facilityId, name: unitName, code: unitCode, unit_type: "ward" });
            setUnitId(response.data.uuid); setUnitName(""); setUnitCode(""); setNotice("Ward created. Continue with a room.");
          }); }}>
            <div className="border rounded-3 p-3"><div className="d-flex align-items-center gap-2 mb-3"><span className="badge rounded-pill text-bg-light border">2</span><h3 className="h6 mb-0">Ward or unit</h3></div>
              <label className="form-label small" htmlFor="unit-facility">Facility</label><select id="unit-facility" className="form-select mb-2" required value={facilityId} onChange={(event) => { setFacilityId(event.target.value); setUnitId(""); setRoomId(""); }}><option value="">Choose facility</option>{facilities.map((item) => <option key={item.uuid} value={item.uuid}>{item.name} ({item.code})</option>)}</select>
              <label className="form-label small" htmlFor="unit-template">Unit</label><select id="unit-template" className="form-select" required value={unitCode} onChange={(event) => { const option = catalog.units.find((item) => item.code === event.target.value); setUnitName(option?.name ?? ""); setUnitCode(option?.code ?? ""); }}><option value="">Choose ward or unit</option>{catalog.units.map((item) => <option key={item.id} value={item.code}>{item.name} ({item.code})</option>)}</select>
              <button className="btn btn-outline-primary w-100 mt-3" disabled={saving || !facilityId}>Create ward</button>
            </div>
          </form>
          <form className="col-12 col-md-6 col-xl-3" onSubmit={(event) => { event.preventDefault(); void submit(async () => {
            const response = await apiClient.axios.post<Room>("/hospital-operations/rooms/setup/", { facility: facilityId, unit: unitId, number: roomNumber });
            setRoomId(response.data.uuid); setRoomNumber(""); setNotice("Room created. Continue with a bed.");
          }); }}>
            <div className="border rounded-3 p-3"><div className="d-flex align-items-center gap-2 mb-3"><span className="badge rounded-pill text-bg-light border">3</span><h3 className="h6 mb-0">Room</h3></div>
              <label className="form-label small" htmlFor="room-unit">Ward or unit</label><select id="room-unit" className="form-select mb-2" required value={unitId} onChange={(event) => { setUnitId(event.target.value); setRoomId(""); }}><option value="">Choose ward</option>{scopedUnits.map((item) => <option key={item.uuid} value={item.uuid}>{item.name} ({item.code})</option>)}</select>
              <label className="form-label small" htmlFor="room-template">Room</label><select id="room-template" className="form-select mb-3" required value={roomNumber} onChange={(event) => setRoomNumber(event.target.value)}><option value="">Choose room</option>{catalog.rooms.map((item) => <option key={item.id} value={item.code}>{item.name}</option>)}</select>
              <button className="btn btn-outline-primary w-100" disabled={saving || !unitId}>Create room</button>
            </div>
          </form>
          <form className="col-12 col-md-6 col-xl-3" onSubmit={(event) => { event.preventDefault(); void submit(async () => {
            await apiClient.axios.post("/hospital-operations/beds/setup/", { room: roomId, label: bedLabel });
            setBedLabel(""); setNotice("Bed created and ready for assignment.");
          }); }}>
            <div className="border rounded-3 p-3"><div className="d-flex align-items-center gap-2 mb-3"><span className="badge rounded-pill text-bg-light border">4</span><h3 className="h6 mb-0">Bed</h3></div>
              <label className="form-label small" htmlFor="bed-room">Room</label><select id="bed-room" className="form-select mb-2" required value={roomId} onChange={(event) => setRoomId(event.target.value)}><option value="">Choose room</option>{scopedRooms.map((item) => <option key={item.uuid} value={item.uuid}>Room {item.number}</option>)}</select>
              <label className="form-label small" htmlFor="bed-template">Bed</label><select id="bed-template" className="form-select mb-3" required value={bedLabel} onChange={(event) => setBedLabel(event.target.value)}><option value="">Choose bed</option>{catalog.beds.map((item) => <option key={item.id} value={item.code}>{item.name}</option>)}</select>
              <button className="btn btn-primary w-100" disabled={saving || !roomId}>Create bed</button>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}

function AdmissionForm() {
  const { bootstrap, isError: isBootstrapError, error: bootstrapError } = useBootstrap();
  const tenantId = bootstrap?.tenant?.id;
  const organizationId = bootstrap?.organization?.id;
  const [patients, setPatients] = useState<AdmissionPatient[]>([]);
  const [units, setUnits] = useState<AdmissionUnit[]>([]);
  const [rooms, setRooms] = useState<AdmissionRoom[]>([]);
  const [beds, setBeds] = useState<AdmissionBed[]>([]);
  const [patientId, setPatientId] = useState("");
  const [unitId, setUnitId] = useState("");
  const [bedId, setBedId] = useState("");
  const [admissionNumber, setAdmissionNumber] = useState("");
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const bootstrapContextError = !bootstrap && isBootstrapError
    ? bootstrapError?.message ?? "Unable to load tenant context."
    : bootstrap && (!tenantId || !organizationId)
      ? "Tenant and organization context are required to admit a patient."
      : null;

  const loadOptions = useCallback(async () => {
    if (!tenantId || !organizationId) return;

    const user = authRuntime.userStorage.updateUser({ tenantId, organizationId });
    if (!user) {
      setError("Authenticated user context is unavailable. Please sign in again.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const [patientResponse, unitResponse, roomResponse, bedResponse] = await Promise.all([
        apiClient.axios.get<ApiCollection<Record<string, unknown>>>(`${patientEndpoints.collection}?page_size=100&is_active=true`),
        apiClient.axios.get<ApiCollection<Record<string, unknown>>>("/hospital-operations/units/"),
        apiClient.axios.get<ApiCollection<Record<string, unknown>>>("/hospital-operations/rooms/"),
        apiClient.axios.get<ApiCollection<Record<string, unknown>>>("/hospital-operations/beds/"),
      ]);

      setPatients(collectionRows(patientResponse.data).map((patient) => ({
        id: String(patient.id ?? ""),
        label: `${String(patient.display_name ?? "Patient")} · ${String(patient.mrn ?? "")}`,
      })).filter((patient) => patient.id));
      setUnits(collectionRows(unitResponse.data).map((unit) => ({
        uuid: String(unit.uuid ?? ""),
        name: String(unit.name ?? "Unit"),
        active: Boolean(unit.active),
      })).filter((unit) => unit.uuid && unit.active));
      setRooms(collectionRows(roomResponse.data).map((room) => ({
        uuid: String(room.uuid ?? ""),
        unit: String(room.unit ?? ""),
        number: String(room.number ?? ""),
      })).filter((room) => room.uuid && room.unit));
      setBeds(collectionRows(bedResponse.data).map((bed) => ({
        uuid: String(bed.uuid ?? ""),
        room: String(bed.room ?? ""),
        label: String(bed.label ?? "Bed"),
        status: String(bed.status ?? ""),
      })).filter((bed) => bed.uuid && bed.room));
    } catch (loadError) {
      setError(messageFrom(loadError));
    } finally {
      setLoading(false);
    }
  }, [tenantId, organizationId]);

  useEffect(() => {
    if (tenantId && organizationId) {
      void Promise.resolve().then(loadOptions);
    }
  }, [loadOptions, organizationId, tenantId]);

  const availableBeds = useMemo(
    () => beds.filter((bed) => rooms.some((room) => room.uuid === bed.room && room.unit === unitId)),
    [beds, rooms, unitId],
  );

  async function submitAdmission(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError(null);
    setNotice(null);
    try {
      const response = await apiClient.axios.post<{ admission_number: string }>(
        "/hospital-operations/admissions/",
        {
          patient: patientId,
          unit: unitId,
          bed: bedId,
          admission_number: admissionNumber.trim(),
          reason: reason.trim(),
        },
      );
      setNotice(`Admission ${response.data.admission_number} created and bed assigned.`);
      setBedId("");
      setAdmissionNumber("");
      setReason("");
      await loadOptions();
    } catch (submitError) {
      setError(messageFrom(submitError));
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="card border-0 shadow-sm mt-4" aria-label="Admit patient to a bed">
      <div className="card-body p-4">
        <div className="text-primary small text-uppercase fw-semibold mb-1">Inpatient admission</div>
        <h2 className="h4 mb-1">Assign a patient to an available bed</h2>
        <p className="text-body-secondary mb-4">Choose a patient and ward, then select an available bed. Admission will occupy the bed.</p>
        {bootstrapContextError || error ? <div className="alert alert-danger" role="alert">{bootstrapContextError ?? error}</div> : null}
        {notice ? <div className="alert alert-success" role="status">{notice}</div> : null}
        {loading ? <p className="text-body-secondary" role="status">Loading patients and available beds…</p> : null}
        <form onSubmit={(event) => void submitAdmission(event)}>
          <div className="row g-3">
            <div className="col-12 col-md-6 col-xl-3">
              <label className="form-label" htmlFor="admission-patient">Patient</label>
              <select id="admission-patient" className="form-select" required value={patientId} onChange={(event) => setPatientId(event.target.value)} disabled={loading || patients.length === 0}>
                <option value="">Choose patient</option>
                {patients.map((patient) => <option key={patient.id} value={patient.id}>{patient.label}</option>)}
              </select>
              {!loading && patients.length === 0 ? <div className="form-text">No patients found for this organization.</div> : null}
            </div>
            <div className="col-12 col-md-6 col-xl-3">
              <label className="form-label" htmlFor="admission-unit">Ward or unit</label>
              <select id="admission-unit" className="form-select" required value={unitId} onChange={(event) => { setUnitId(event.target.value); setBedId(""); }} disabled={loading || units.length === 0}>
                <option value="">Choose ward or unit</option>
                {units.map((unit) => <option key={unit.uuid} value={unit.uuid}>{unit.name}</option>)}
              </select>
            </div>
            <div className="col-12 col-md-6 col-xl-3">
              <label className="form-label" htmlFor="admission-bed">Available bed</label>
              <select id="admission-bed" className="form-select" required value={bedId} onChange={(event) => setBedId(event.target.value)} disabled={loading || !unitId || availableBeds.length === 0}>
                <option value="">Choose available bed</option>
                {availableBeds.map((bed) => {
                  const room = rooms.find((item) => item.uuid === bed.room);
                  return <option key={bed.uuid} value={bed.uuid}>Room {room?.number} · {bed.label}</option>;
                })}
              </select>
              {unitId && availableBeds.length === 0 ? <div className="form-text">No available beds in this ward.</div> : null}
            </div>
            <div className="col-12 col-md-6 col-xl-3">
              <label className="form-label" htmlFor="admission-number">Admission number</label>
              <input id="admission-number" className="form-control" required maxLength={80} value={admissionNumber} onChange={(event) => setAdmissionNumber(event.target.value)} placeholder="e.g. ADM-2026-001" />
            </div>
            <div className="col-12">
              <label className="form-label" htmlFor="admission-reason">Reason <span className="text-body-secondary">(optional)</span></label>
              <textarea id="admission-reason" className="form-control" rows={2} value={reason} onChange={(event) => setReason(event.target.value)} />
            </div>
            <div className="col-12">
              <button className="btn btn-primary" type="submit" disabled={saving || loading || !patientId || !unitId || !bedId || !admissionNumber.trim()}>
                {saving ? "Admitting…" : "Admit patient and assign bed"}
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>
  );
}

export function HospitalOperationsBusinessWorkspace({
  module,
}: HospitalOperationsBusinessWorkspaceProps) {
  void hospitalOperationsRuntimeContract;

  return (
    <section className="container-fluid py-4">
      <header className="d-flex flex-column flex-lg-row justify-content-between align-items-lg-end gap-3 mb-4">
        <div>
          <div className="text-primary small text-uppercase fw-semibold mb-1">Hospital operations</div>
          <h1 className="h2 mb-1">Capacity and bed management</h1>
          <p className="text-body-secondary mb-0">Configure care locations and maintain real-time bed availability for {module.displayName}.</p>
        </div>
        <span className="badge text-bg-light border rounded-pill px-3 py-2">Backend-authorized</span>
      </header>

      <CapacitySetup />

  <AdmissionForm />

      <div className="card border-0 shadow-sm mt-4">
        <div className="card-header bg-body border-bottom py-3 d-flex justify-content-between align-items-center">
          <div><h2 className="h5 mb-0">Bed availability</h2><span className="small text-body-secondary">Available beds will appear here after configuration.</span></div>
        </div>
        <div className="card-body">
          <ModuleDataTable
            module={module}
            route="/hospital-operations/beds/"
            table={{
              columns: [
                { id: "bed_number", label: "Bed" },
                { id: "status", label: "Status" },
                { id: "room", label: "Room" },
                { id: "unit", label: "Unit" },
              ],
              emptyMessage: "No available beds are configured for this organization.",
            }}
          />
        </div>
      </div>
    </section>
  );
}
