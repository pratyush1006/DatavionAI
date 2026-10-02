import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const features = [
  ["Clinical operations", "Patient journeys, clinical workflows, scheduling, coordination, and operational context."],
  ["Revenue cycle", "Billing, finance operations, collections, payments, and revenue visibility."],
  ["Pharmacy", "Department-owned workflows and focused pharmacy intelligence."],
  ["Laboratory", "Lab workflows, orders, operational tracking, and connected clinical context."],
  ["Workforce", "Employees, departments, teams, permissions, and organization structure."],
  ["Documents", "Connected document workflows and enterprise storage capabilities."],
  ["Analytics", "KPIs, reports, dashboards, and operational command-center visibility."],
  ["AI assistants", "Retrieval, intelligent search, workflow assistance, and department-aware AI."],
];

export default function FeaturesPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Platform</div>
          <h1>Capabilities that work together instead of sitting in silos.</h1>
          <p>
            DatavionOS brings healthcare capabilities into one operating
            layer while keeping access and experiences focused by organization,
            department, subscription, and role.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="capability-grid">
            {features.map(([title, description], index) => (
              <article className="capability-card" key={title}>
                <span className="capability-number">{String(index + 1).padStart(2, "0")}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Architecture"
            title="Backend-driven at the center. Human-friendly at the surface."
            description="The target frontend behavior is simple: render what the backend says the organization can use."
          />

          <div className="architecture-wide">
            {[
              ["01", "Organization context", "Defines the healthcare organization and operating environment."],
              ["02", "Subscription", "Defines the commercial entitlement envelope."],
              ["03", "Modules", "Defines capabilities enabled within the organization."],
              ["04", "Roles", "Defines who can access which capability."],
            ].map(([number, title, description]) => (
              <div key={number} className="architecture-wide-card">
                <span>{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <div className="final-cta">
            <div className="section-eyebrow section-eyebrow-light">See it in action</div>
            <h2>Start with the platform. Grow into the operating system.</h2>
            <p>Register your organization or explore how DatavionOS fits different healthcare environments.</p>
            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">Register organization</Button>
              <Button href="/solutions" variant="outline-light">Explore solutions</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
