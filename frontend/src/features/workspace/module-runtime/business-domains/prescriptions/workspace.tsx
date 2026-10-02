import type { ModuleRuntimeDefinition } from "../../domain/types";
import { useCallback, useEffect, useState } from "react";
import { apiClient } from "@/core/api";
import type { PrescriptionsAiBoundary } from "./types";

type PrescriptionRow = {
  id: string;
  prescription_number: string;
  status: string;
  encounter: string;
  is_verified: boolean;
  verified_at: string | null;
};

function PrescriptionVerificationPanel() {
  const [rows, setRows] = useState<PrescriptionRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<string>();
  const [error, setError] = useState<string>();

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apiClient.axios.get<PrescriptionRow[]>("/prescriptions/");
      setRows(response.data);
      setError(undefined);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to load prescriptions.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const startup = window.setTimeout(() => void refresh(), 0);
    return () => window.clearTimeout(startup);
  }, [refresh]);

  const verify = async (prescription: PrescriptionRow) => {
    setBusyId(prescription.id);
    setError(undefined);
    try {
      await apiClient.axios.post(
        `/prescriptions/${prescription.id}/lifecycle/`,
        { target: "verify" },
      );
      await refresh();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Prescription verification failed.");
    } finally {
      setBusyId(undefined);
    }
  };

  return (
    <section className="card shadow-sm mb-3" aria-label="Prescription verification">
      <div className="card-body">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <div>
            <h2 className="h6 mb-1">Doctor verification</h2>
            <p className="small text-body-secondary mb-0">
              Verifying the last prescription on an in-progress encounter automatically checks out the appointment.
            </p>
          </div>
          <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => void refresh()} disabled={loading}>
            Refresh
          </button>
        </div>
        {error && <div className="alert alert-warning" role="alert">{error}</div>}
        {loading ? <p className="text-body-secondary">Loading prescriptions…</p> : rows.length === 0 ? (
          <p className="text-body-secondary">No prescriptions are available.</p>
        ) : (
          <div className="table-responsive">
            <table className="table table-sm align-middle mb-0">
              <thead><tr><th>Prescription</th><th>Encounter</th><th>Verification</th><th /></tr></thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td>{row.prescription_number}</td>
                    <td>{row.encounter}</td>
                    <td>{row.is_verified ? `Verified${row.verified_at ? ` · ${new Date(row.verified_at).toLocaleString()}` : ""}` : "Needs doctor verification"}</td>
                    <td className="text-end">
                      {!row.is_verified && (
                        <button type="button" className="btn btn-primary btn-sm" disabled={busyId === row.id} onClick={() => void verify(row)}>
                          {busyId === row.id ? "Verifying…" : "Verify & check out"}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </section>
  );
}

export type PrescriptionsBusinessWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;

const prescriptionsAiBoundary: PrescriptionsAiBoundary = {
  department: "prescriptions",
  owner: "prescriptions",
  enabledByOrganization: false,
};

export function PrescriptionsBusinessWorkspace({
  module,
}: PrescriptionsBusinessWorkspaceProps) {
  return (
    <section className="container-fluid py-3">
      <div className="row g-3 mb-3">
        <div className="col-12">
          <div className="d-flex flex-wrap justify-content-between align-items-start gap-3">
            <div>
              <div className="text-body-secondary small text-uppercase fw-semibold">
                Prescriptions workspace
              </div>
              <h1 className="h3 mb-1">Prescriptions</h1>
              <p className="text-body-secondary mb-0">
                Prescription records exposed through the canonical
                Prescriptions API contract.
              </p>
            </div>
            <span className="badge text-bg-light border">
              {module.displayName}
            </span>
          </div>
        </div>
      </div>

      <div className="row g-3 mb-3">
        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Workspace</div>
              <div className="fs-5 fw-semibold">Prescriptions</div>
              <div className="small text-body-secondary mt-1">
                Dynamic Bootstrap clinical module
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">Data source</div>
              <div className="fs-6 fw-semibold">Canonical API adapter</div>
              <div className="small text-body-secondary mt-1">
                Read-only workspace data
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-md-4">
          <div className="card h-100 shadow-sm">
            <div className="card-body">
              <div className="text-body-secondary small">
                Prescriptions AI
              </div>
              <div className="fs-6 fw-semibold">Department-scoped</div>
              <div className="small text-body-secondary mt-1">
                Backend-controlled capability boundary
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="card shadow-sm">
        <div className="card-body">
          <PrescriptionVerificationPanel />
        </div>
      </div>

      <div className="card shadow-sm mt-3 border-start border-4">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-start gap-3">
            <div>
              <h2 className="h6 mb-1">Prescriptions AI</h2>
              <p className="small text-body-secondary mb-0">
                AI availability is controlled by backend effective capability
                context and organization configuration. This workspace does
                not grant or infer access.
              </p>
            </div>
            <span className="badge text-bg-secondary">
              {prescriptionsAiBoundary.department}
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
