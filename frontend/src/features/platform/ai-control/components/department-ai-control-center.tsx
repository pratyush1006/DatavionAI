"use client";

import { useEffect, useState } from "react";

import {
  getAIControlSnapshot,
  setAIApplicationEnabled,
} from "../api";

import type {
  AIControlSnapshot,
} from "../domain";


export function DepartmentAIControlCenter() {
  const [data, setData] =
    useState<AIControlSnapshot | null>(null);

  const [error, setError] = useState("");
  const [busy, setBusy] = useState("");


  useEffect(() => {
    let cancelled = false;

    void getAIControlSnapshot()
      .then((snapshot) => {
        if (cancelled) {
          return;
        }

        setData(snapshot);
        setError("");
      })
      .catch((exception) => {
        if (cancelled) {
          return;
        }

        setError(
          exception instanceof Error
            ? exception.message
            : "Unable to load AI controls.",
        );
      });

    return () => {
      cancelled = true;
    };
  }, []);


  async function toggle(
    applicationId: string,
    enabled: boolean,
  ) {
    setBusy(applicationId);
    setError("");

    try {
      const snapshot =
        await setAIApplicationEnabled(
          applicationId,
          enabled,
        );

      setData(snapshot);
    } catch (exception) {
      setError(
        exception instanceof Error
          ? exception.message
          : "Unable to update AI capability.",
      );
    } finally {
      setBusy("");
    }
  }


  if (!data && !error) {
    return (
      <div className="container-fluid py-4">
        Loading department AI controls...
      </div>
    );
  }


  if (!data) {
    return (
      <div className="container-fluid py-4">
        <div className="alert alert-danger">
          {error}
        </div>
      </div>
    );
  }


  return (
    <div className="container-fluid py-4">
      <h1 className="h3 mb-1">
        Department AI
      </h1>

      <p className="text-muted mb-4">
        {data.organization.name}
        {" · "}
        Domain-owned AI controls
      </p>

      {error && (
        <div className="alert alert-danger">
          {error}
        </div>
      )}

      <div className="row g-4">
        {data.capabilities.map((item) => {
          const blocked =
            !item.entitled ||
            !item.module_enabled ||
            !item.feature_enabled;

          return (
            <div
              className="col-12 col-xl-6"
              key={item.id}
            >
              <div className="card h-100 shadow-sm">
                <div className="card-body">
                  <div className="d-flex justify-content-between">
                    <div>
                      <h2 className="h5 mb-1">
                        {item.name}
                      </h2>

                      <div className="small text-muted">
                        Owner: {item.department}
                      </div>
                    </div>

                    <div className="form-check form-switch">
                      <input
                        className="form-check-input"
                        type="checkbox"
                        role="switch"
                        checked={
                          item.organization_enabled
                        }
                        disabled={
                          !data.can_manage_ai ||
                          blocked ||
                          busy === item.id
                        }
                        onChange={(event) =>
                          void toggle(
                            item.id,
                            event.target.checked,
                          )
                        }
                        aria-label={`Toggle ${item.name}`}
                      />
                    </div>
                  </div>

                  <div className="d-flex flex-wrap gap-2 mt-3">
                    <span
                      className={`badge ${
                        item.entitled
                          ? "text-bg-success"
                          : "text-bg-secondary"
                      }`}
                    >
                      {item.entitled
                        ? "Entitled"
                        : "Not entitled"}
                    </span>

                    <span
                      className={`badge ${
                        item.module_enabled
                          ? "text-bg-success"
                          : "text-bg-warning"
                      }`}
                    >
                      Module{" "}
                      {item.module_enabled
                        ? "ON"
                        : "OFF"}
                    </span>

                    <span
                      className={`badge ${
                        item.feature_enabled
                          ? "text-bg-success"
                          : "text-bg-warning"
                      }`}
                    >
                      Feature{" "}
                      {item.feature_enabled
                        ? "ON"
                        : "OFF"}
                    </span>

                    <span
                      className={`badge ${
                        item.department_access
                          ? "text-bg-success"
                          : "text-bg-secondary"
                      }`}
                    >
                      Department{" "}
                      {item.department_access
                        ? "matched"
                        : "restricted"}
                    </span>
                  </div>

                  <div className="small text-muted mt-3">
                    Requires{" "}
                    {item.required_module}
                    {" · "}
                    {item.required_feature}
                    {" · "}
                    {item.required_permission}
                  </div>

                  {item.human_review_required && (
                    <div className="alert alert-warning mt-3 mb-0">
                      Human review is required for
                      this capability.
                    </div>
                  )}

                  {blocked && (
                    <div className="small text-muted mt-3">
                      Required
                      subscription/module/feature
                      prerequisites are not active.
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
