"use client";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { useState } from "react";

import {
  fetchOrganizationControlPlane,
  organizationControlKeys,
  toggleOrganizationFeature,
  toggleOrganizationModule,
} from "../api";

import type {
  OrganizationControlFeature,
  OrganizationControlModule,
} from "../domain";

function label(code: string, name?: string | null): string {
  if (name?.trim()) {
    return name;
  }

  return code
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function isEnabled(status: string): boolean {
  return status === "enabled" || status === "trial";
}

function StatusBadge({ status }: { status: string }) {
  const normalized = status.toLowerCase();

  if (normalized === "enabled" || normalized === "trial") {
    return <span className="badge text-bg-success">{status}</span>;
  }

  if (normalized === "locked") {
    return (
      <span className="badge text-bg-warning">
        Upgrade required
      </span>
    );
  }

  return (
    <span className="badge text-bg-secondary">
      {status}
    </span>
  );
}

function ModuleRow({
  item,
  allowed,
  pending,
  onToggle,
}: {
  item: OrganizationControlModule;
  allowed: boolean;
  pending: boolean;
  onToggle: () => void;
}) {
  const active = isEnabled(item.status);
  const locked = item.status === "locked";

  return (
    <div className="border rounded-3 p-3 mb-3">
      <div className="d-flex justify-content-between align-items-center gap-3">
        <div className="min-w-0">
          <div className="fw-semibold">
            {label(item.module_code)}
          </div>
          <div className="small text-body-secondary mt-1">
            <StatusBadge status={item.status} />
          </div>
        </div>

        <button
          type="button"
          className={`btn btn-sm ${
            active
              ? "btn-success"
              : "btn-outline-secondary"
          }`}
          disabled={!allowed || locked || pending}
          onClick={onToggle}
          aria-pressed={active}
        >
          {pending
            ? "Saving..."
            : active
              ? "ON"
              : "OFF"}
        </button>
      </div>
    </div>
  );
}

function FeatureRow({
  item,
  allowed,
  pending,
  onToggle,
}: {
  item: OrganizationControlFeature;
  allowed: boolean;
  pending: boolean;
  onToggle: () => void;
}) {
  const active = isEnabled(item.status);
  const locked = item.status === "locked";

  return (
    <div className="border rounded-3 p-3 mb-3">
      <div className="d-flex justify-content-between align-items-center gap-3">
        <div className="min-w-0">
          <div className="fw-semibold">
            {label(
              item.feature_code,
              item.feature_name,
            )}
          </div>
          <div className="small text-body-secondary mt-1">
            <StatusBadge status={item.status} />
          </div>
        </div>

        <button
          type="button"
          className={`btn btn-sm ${
            active
              ? "btn-success"
              : "btn-outline-secondary"
          }`}
          disabled={!allowed || locked || pending}
          onClick={onToggle}
          aria-pressed={active}
        >
          {pending
            ? "Saving..."
            : active
              ? "ON"
              : "OFF"}
        </button>
      </div>
    </div>
  );
}

export function OrganizationCapabilityControlCenter() {
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const query = useQuery({
    queryKey: organizationControlKeys.snapshot(),
    queryFn: fetchOrganizationControlPlane,
  });

  const moduleMutation = useMutation({
    mutationFn: toggleOrganizationModule,
    onSuccess: async () => {
      setError(null);
      await queryClient.invalidateQueries({
        queryKey: organizationControlKeys.snapshot(),
      });
      await queryClient.invalidateQueries({
        queryKey: ["platform", "bootstrap"],
      });
    },
    onError: (value) => {
      setError(
        value instanceof Error
          ? value.message
          : "Unable to update the organization module.",
      );
    },
  });

  const featureMutation = useMutation({
    mutationFn: toggleOrganizationFeature,
    onSuccess: async () => {
      setError(null);
      await queryClient.invalidateQueries({
        queryKey: organizationControlKeys.snapshot(),
      });
      await queryClient.invalidateQueries({
        queryKey: ["platform", "bootstrap"],
      });
    },
    onError: (value) => {
      setError(
        value instanceof Error
          ? value.message
          : "Unable to update the organization feature.",
      );
    },
  });

  if (query.isLoading) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-light border">
          Loading organization capabilities...
        </div>
      </div>
    );
  }

  if (query.isError || !query.data) {
    const message = query.error instanceof Error
      ? query.error.message
      : "Unable to load the organization control plane.";
    return (
      <div className="container-fluid py-4">
        <div className="small text-body-secondary text-uppercase fw-semibold">Organization administration</div>
        <h1 className="h3 mb-1">Modules &amp; Features</h1>
        <p className="text-body-secondary">Manage capabilities provisioned for the active organization.</p>
        <div className="alert alert-danger">
          <div className="fw-semibold mb-1">Organization capabilities could not be loaded</div>
          <div>{message}</div>
          <button type="button" className="btn btn-sm btn-outline-danger mt-3" onClick={() => void query.refetch()}>
            Try again
          </button>
        </div>
      </div>
    );
  }

  const snapshot = query.data;

  return (
    <div className="container-fluid py-4">
      <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
        <div>
          <div className="small text-body-secondary text-uppercase fw-semibold">
            Organization Administration
          </div>
          <h1 className="h3 mb-1">
            Modules &amp; Features
          </h1>
          <p className="text-body-secondary mb-0">
            Manage capabilities already provisioned for this organization.
          </p>
        </div>

        <div className="text-end">
          <div className="fw-semibold">
            {snapshot.organization.display_name}
          </div>
          <div className="small text-body-secondary">
            {snapshot.organization.organization_type}
          </div>
        </div>
      </div>

      {snapshot.subscription ? (
        <div className="card border-0 shadow-sm mb-4">
          <div className="card-body">
            <div className="row g-3">
              <div className="col-md-4">
                <div className="small text-body-secondary">
                  Plan
                </div>
                <div className="fw-semibold">
                  {snapshot.subscription.plan.name ??
                    snapshot.subscription.plan.code ??
                    "Current subscription"}
                </div>
              </div>

              <div className="col-md-4">
                <div className="small text-body-secondary">
                  Status
                </div>
                <div className="fw-semibold">
                  {snapshot.subscription.status}
                </div>
              </div>

              <div className="col-md-4">
                <div className="small text-body-secondary">
                  Healthcare segment
                </div>
                <div className="fw-semibold">
                  {snapshot.subscription.plan.healthcare_segment ??
                    "—"}
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="alert alert-warning">
          No active subscription snapshot is available.
        </div>
      )}

      {error ? (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      ) : null}

      <div className="row g-4">
        <div className="col-12 col-xl-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h2 className="h5 mb-1">Modules</h2>
                  <p className="small text-body-secondary mb-0">
                    Organization-level ON/OFF controls.
                  </p>
                </div>
                <span className="badge text-bg-light border">
                  {snapshot.modules.length}
                </span>
              </div>

              {snapshot.modules.length === 0 ? (
                <div className="small text-body-secondary">
                  No organization module assignments were returned.
                </div>
              ) : (
                snapshot.modules.map((item) => (
                  <ModuleRow
                    key={item.id}
                    item={item}
                    allowed={snapshot.can_manage_modules}
                    pending={
                      moduleMutation.isPending &&
                      moduleMutation.variables?.id === item.id
                    }
                    onToggle={() =>
                      moduleMutation.mutate({
                        id: item.id,
                        enabled: !isEnabled(item.status),
                      })
                    }
                  />
                ))
              )}
            </div>
          </div>
        </div>

        <div className="col-12 col-xl-6">
          <div className="card border-0 shadow-sm h-100">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h2 className="h5 mb-1">Features</h2>
                  <p className="small text-body-secondary mb-0">
                    Feature-level organization controls.
                  </p>
                </div>
                <span className="badge text-bg-light border">
                  {snapshot.features.length}
                </span>
              </div>

              {snapshot.features.length === 0 ? (
                <div className="small text-body-secondary">
                  No organization feature assignments were returned.
                </div>
              ) : (
                snapshot.features.map((item) => (
                  <FeatureRow
                    key={item.id}
                    item={item}
                    allowed={snapshot.can_manage_features}
                    pending={
                      featureMutation.isPending &&
                      featureMutation.variables?.id === item.id
                    }
                    onToggle={() =>
                      featureMutation.mutate({
                        id: item.id,
                        enabled: !isEnabled(item.status),
                      })
                    }
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="alert alert-light border mt-4 mb-0">
        <strong>Security boundary:</strong> this UI only sends organization
        control requests. Subscription entitlement, tenant isolation and RBAC
        remain backend-enforced.
      </div>

      {!snapshot.can_manage_modules && !snapshot.can_manage_features ? (
        <div className="alert alert-warning mt-3 mb-0">
          Your current role can view this organization&apos;s provisioned capabilities but cannot change them. Platform administration is separate from organization-level module administration.
        </div>
      ) : null}
    </div>
  );
}
