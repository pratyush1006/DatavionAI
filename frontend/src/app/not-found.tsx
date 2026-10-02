import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-vh-100 d-flex align-items-center justify-content-center bg-body-tertiary p-4">
      <section className="card border-0 shadow-sm" style={{ maxWidth: 520 }}>
        <div className="card-body p-4 p-md-5 text-center">
          <p className="text-primary fw-semibold text-uppercase small">404</p>
          <h1 className="h3">Page not found</h1>
          <p className="text-body-secondary mb-4">
            The page may have moved, or you may not have access to it.
          </p>
          <Link className="btn btn-primary" href="/dashboard">
            Go to dashboard
          </Link>
        </div>
      </section>
    </main>
  );
}
