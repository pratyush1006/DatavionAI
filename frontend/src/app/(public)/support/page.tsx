import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const areas = [
  ["Sales & onboarding", "Questions about organization registration, product fit, pricing, or getting started."],
  ["Product support", "Help with platform usage, modules, accounts, and operational workflows."],
  ["Enterprise", "Questions about broader deployments, organization structures, and integrations."],
  ["Careers", "Connect with the team about opportunities and roles."],
];

export default function SupportPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Support</div>
          <h1>Get the right DatavionAI team in the loop.</h1>
          <p>
            Start with the area closest to your question, then continue into
            organization registration or your existing account.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="support-grid">
            {areas.map(([title, description]) => (
              <article className="support-card" key={title}>
                <h2>{title}</h2>
                <p>{description}</p>
                <a href="mailto:support@datavion.ai">Contact team ↗</a>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Getting started"
            title="The fastest path usually starts with your organization."
            description="Registration establishes the organization context the backend can use to shape the product experience."
          />

          <div className="journey-grid">
            {[
              ["01", "Register", "Create your organization profile."],
              ["02", "Review", "Complete onboarding and commercial steps."],
              ["03", "Configure", "Enable capabilities your organization needs."],
              ["04", "Operate", "Use DatavionOS from one connected foundation."],
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
            <div className="section-eyebrow section-eyebrow-light">Ready?</div>
            <h2>Start your organization journey.</h2>
            <p>Register a new organization or log in to an existing account.</p>
            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">Register organization</Button>
              <Button href="/login" variant="outline-light">Log in</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
