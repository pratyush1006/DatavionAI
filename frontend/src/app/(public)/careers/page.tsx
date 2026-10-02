import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const values = [
  ["Build for real work", "Solve workflow problems people actually experience."],
  ["Think in systems", "Design for dependencies between people, data, and departments."],
  ["Own the outcome", "Take responsibility from architecture through experience."],
  ["Use AI carefully", "Make intelligence useful, grounded, and context-aware."],
];

const teams = [
  ["Engineering", "Platform, API, frontend, data, AI, infrastructure, and enterprise systems."],
  ["Product & Design", "Healthcare workflows, information architecture, and user experience."],
  ["AI & Data", "Retrieval, intelligence, analytics, and automation experiences."],
  ["Customer Success", "Helping healthcare organizations turn operational needs into outcomes."],
];

export default function CareersPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Careers</div>
          <h1>Help build the operating system healthcare organizations can grow on.</h1>
          <p>
            We are building for hard systems problems, thoughtful design,
            and technology that changes how teams operate.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <SectionTitle
            eyebrow="How we work"
            title="High ownership. Strong systems thinking. Real users."
            description="We want people who can move between architecture, implementation, and experience without losing sight of the problem."
          />

          <div className="principle-grid">
            {values.map(([title, description]) => (
              <div className="principle-card" key={title}>
                <h3>{title}</h3>
                <p>{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Teams"
            title="Where we are building."
            description="Open roles change over time. Start a conversation even when a specific role is not listed."
          />

          <div className="team-grid">
            {teams.map(([title, description]) => (
              <div className="team-card" key={title}>
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
            <div className="section-eyebrow section-eyebrow-light">Join us</div>
            <h2>Build something meaningful with the team.</h2>
            <p>Start a conversation with DatavionAI.</p>
            <div className="hero-buttons">
              <Button href="/support" variant="light">Contact the team</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
