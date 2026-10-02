
import Link from "next/link";

export default function ModuleWorkspaceNotFound() {
  return (
    <section className="container-fluid py-5">
      <div className="row justify-content-center">
        <div className="col-12 col-lg-7 col-xl-6">
          <div className="card border-0 shadow-sm text-center">
            <div className="card-body p-5">
              <div className="display-6 fw-semibold mb-3">
                Workspace not found
              </div>

              <p className="text-body-secondary mb-4">
                This workspace is not present in the current
                DatavionOS Bootstrap context.
              </p>

              <Link
                href="/dashboard"
                className="btn btn-primary"
              >
                Return to dashboard
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
