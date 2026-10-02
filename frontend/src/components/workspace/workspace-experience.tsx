/**
 * DatavionOS authenticated workspace presentation boundary.
 * Backend bootstrap remains authoritative for runtime capability and navigation.
 */

"use client";

import { RefreshCw, ShieldCheck } from "lucide-react";
import type { ReactNode } from "react";
import { useBootstrap } from "@/core/bootstrap";

type Props = Readonly<{ children: ReactNode }>;

function LoadingWorkspace() {
  return (
    <div className="container-fluid py-4" aria-busy="true">
      <div className="row g-4">
        <div className="col-12">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <div className="placeholder-glow" aria-hidden="true">
                <span className="placeholder col-4 d-block mb-3" />
                <span className="placeholder col-8 d-block mb-2" />
                <span className="placeholder col-6 d-block" />
              </div>
              <p className="text-body-secondary mb-0 mt-3">
                Preparing your DatavionOS workspace...
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function WorkspaceError({
  message,
  onRetry,
}: Readonly<{ message: string; onRetry: () => void }>) {
  return (
    <div className="container-fluid py-4">
      <div className="row justify-content-center">
        <div className="col-12 col-xl-8">
          <div className="alert alert-danger d-flex align-items-start gap-3 shadow-sm">
            <ShieldCheck size={22} aria-hidden="true" />
            <div className="flex-grow-1">
              <h1 className="h5 mb-1">Workspace unavailable</h1>
              <p className="mb-3">{message}</p>
              <button
                type="button"
                className="btn btn-outline-danger"
                onClick={onRetry}
              >
                <RefreshCw size={16} className="me-2" aria-hidden="true" />
                Retry
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function WorkspaceExperience({ children }: Props) {
  const {
    bootstrap,
    isLoading,
    isFetching,
    isError,
    error,
    refetch,
  } = useBootstrap();

  if (isLoading && bootstrap === null) {
    return <LoadingWorkspace />;
  }

  if (isError && bootstrap === null) {
    return (
      <WorkspaceError
        message={
          error?.message ??
          "The authenticated workspace could not be loaded."
        }
        onRetry={() => {
          void refetch();
        }}
      />
    );
  }

  return (
    <div className="workspace-experience">
      {isFetching && bootstrap !== null ? (
        <div
          className="position-fixed top-0 start-0 w-100"
          style={{ zIndex: 1080 }}
          role="status"
          aria-live="polite"
          aria-label="Refreshing workspace"
        >
          <div className="progress" style={{ height: "3px" }}>
            <div
              className="progress-bar progress-bar-striped progress-bar-animated"
              style={{ width: "100%" }}
            />
          </div>
        </div>
      ) : null}
      {children}
    </div>
  );
}
