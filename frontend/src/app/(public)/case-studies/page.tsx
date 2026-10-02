import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const stories = [
  ["Clinical operations", "Connected workflows", "Bring patient-facing and administrative journeys into one organizational context."],
  ["Pharmacy", "Department-owned AI", "Give pharmacy teams focused intelligent workflows without exposing unrelated modules."],
  ["Revenue cycle", "Shared operating context", "Keep finance operations connected to the organization they support."],
];

export default function CaseStudiesPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Case studies</div>
          <h1>Stories about how the operating model fits real work.</h1>
          <p>
            These are illustrative solution stories that show the DatavionOS
            product model across different healthcare functions.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="case-grid">
            {stories.map(([label, title, description]) => (
              <article className="case-card" key={title}>
                <div className="case-art">
                  <span>{label}</span>
                  <strong>{title}</strong>
                </div>
                <div className="case-content">
                  <p>{description}</p>
                  <span className="case-link">Illustrative solution story ↗</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="The common pattern"
            title="Different departments can share a foundation without sharing every screen."
            description="That is the central idea behind the DatavionOS operating model."
          />
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <div className="final-cta">
            <div className="section-eyebrow section-eyebrow-light">Your organization</div>
            <h2>Build your own DatavionOS operating model.</h2>
            <p>Start registration or explore the platform.</p>
            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">Register organization</Button>
              <Button href="/features" variant="outline-light">Explore platform</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
