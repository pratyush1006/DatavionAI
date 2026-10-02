export default function Loading() {
  return (
    <main
      className="min-vh-100 d-flex align-items-center justify-content-center bg-body-tertiary"
      aria-busy="true"
      aria-live="polite"
    >
      <div className="text-center">
        <div className="spinner-border text-primary" role="status" />
        <p className="mt-3 mb-0 text-body-secondary">Loading DatavionOS…</p>
      </div>
    </main>
  );
}
