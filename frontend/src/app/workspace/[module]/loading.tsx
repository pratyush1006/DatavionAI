
export default function ModuleWorkspaceLoading() {
  return (
    <section className="container-fluid py-4">
      <div className="placeholder-glow mb-4">
        <span className="placeholder col-5 h2" />
        <span className="placeholder col-9" />
      </div>

      <div className="row g-4">
        <div className="col-12 col-xl-8">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <span className="placeholder col-5" />
              <span className="placeholder col-10 mt-3" />
              <span className="placeholder col-8" />

              <div className="row g-3 mt-2">
                <div className="col-12 col-md-6">
                  <span className="placeholder col-12" />
                </div>

                <div className="col-12 col-md-6">
                  <span className="placeholder col-12" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-12 col-xl-4">
          <div className="card border-0 shadow-sm">
            <div className="card-body p-4">
              <span className="placeholder col-6" />
              <span className="placeholder col-10 mt-3" />
              <span className="placeholder col-8" />
              <span className="placeholder col-9" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
