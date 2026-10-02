import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const solutions = [
  ["Clinics", "Focused clinical and administrative operations for organizations that need one connected workspace."],
  ["Hospitals", "Broader department coverage with organization-wide visibility and role-aware operations."],
  ["Pharmacy", "Dedicated pharmacy workflows and AI without exposing unrelated enterprise modules."],
  ["Healthcare groups", "A scalable operating layer for teams, departments, and organizational contexts."],
  ["Operations", "Workforce, tasks, departments, facilities, assets, and cross-functional coordination."],
  ["Leadership", "A command view of the signals and KPIs that matter to organization-level decisions."],
];

export default function SolutionsPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Solutions</div>
          <h1>Different healthcare environments. One connected operating model.</h1>
          <p>
            Start with your organization context and expand into the workflows
            and capabilities that match your actual operating model.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="solution-grid">
            {solutions.map(([title, description]) => (
              <article className="solution-card" key={title}>
                <span className="solution-label">DATAVIONOS</span>
                <h2>{title}</h2>
                <p>{description}</p>
                <div className="solution-points">
                  <span>✓ Modular capabilities</span>
                  <span>✓ Organization-aware</span>
                  <span>✓ AI-ready foundation</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Growth path"
            title="Start focused. Expand without starting over."
            description="The organization gets a common foundation first. New departments and capabilities can be introduced as the organization grows."
          />

          <div className="journey-grid">
            {[
              ["01", "Start", "Register the organization and establish context."],
              ["02", "Configure", "Enable allowed modules and department capabilities."],
              ["03", "Delegate", "Give teams the access and ownership they need."],
              ["04", "Scale", "Extend the workspace as the organization evolves."],
            ].map(([number, title, description]) => (
              <article className="journey-card" key={number}>
                <span>{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <div className="final-cta">
            <div className="section-eyebrow section-eyebrow-light">Start here</div>
            <h2>Build the workspace that matches your organization.</h2>
            <p>Register your organization and begin the onboarding flow.</p>
            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">Register organization</Button>
              <Button href="/pricing" variant="outline-light">View pricing</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
