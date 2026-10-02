import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

export default function AboutPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">About DatavionAI</div>
          <h1>Building the operating layer healthcare organizations can grow on.</h1>
          <p>
            DatavionAI is building DatavionOS as a modular AI operating system
            connecting people, departments, workflows, and intelligent
            capabilities around one organizational context.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="split-section">
            <SectionTitle
              eyebrow="Why we are building it"
              title="Healthcare software should adapt to the organization."
              description="Hospitals, clinics, pharmacies, healthcare groups, and operational teams do not all work the same way. The platform should accommodate that reality."
            />

            <div className="about-card">
              <div><strong>01</strong><span>One foundation</span><p>Shared infrastructure across organization-wide workflows.</p></div>
              <div><strong>02</strong><span>Focused experiences</span><p>Department-specific interfaces and intelligence.</p></div>
              <div><strong>03</strong><span>Flexible growth</span><p>New capabilities without replacing the platform.</p></div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Principles"
            title="A product philosophy grounded in real operating complexity."
            description="The foundation is intentionally designed to support multi-tenant, role-aware, modular, and AI-enabled healthcare operations."
          />

          <div className="principle-grid">
            {[
              ["Modular by design", "Capabilities can be activated around real organizational needs."],
              ["Role aware", "Access should follow the user's role and scope."],
              ["Department focused", "AI and workflows should stay close to the teams that own them."],
              ["Enterprise minded", "Architecture should remain consistent as organizations scale."],
            ].map(([title, description]) => (
              <div className="principle-card" key={title}>
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
            <div className="section-eyebrow section-eyebrow-light">
              Explore DatavionOS
            </div>
            <h2>See the platform from the inside out.</h2>
            <p>Explore the capabilities or register your organization.</p>
            <div className="hero-buttons">
              <Button href="/features" variant="light">Explore platform</Button>
              <Button href="/organization/register" variant="outline-light">
                Register organization
              </Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
