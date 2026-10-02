import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const capabilities = [
  ["01", "Clinical operations", "Connect patient, care, scheduling, clinical, and administrative workflows."],
  ["02", "Revenue cycle", "Bring billing, collections, payments, and financial operations into one context."],
  ["03", "Pharmacy intelligence", "Give pharmacy teams focused workflows and department-owned AI."],
  ["04", "Workforce operations", "Coordinate teams, employees, departments, access, and organization structure."],
  ["05", "AI assistants", "Put retrieval, intelligence, and automation into the workflows that need them."],
  ["06", "Command center", "Turn operational data into a clear management view for leadership."],
];

const journey = [
  ["01", "Register", "Define your organization and its operating context."],
  ["02", "Subscribe", "Choose the commercial tier that fits your organization."],
  ["03", "Configure", "Enable the capabilities your organization wants to operate."],
  ["04", "Operate", "Your workspace adapts to subscription, modules, roles, and permissions."],
];

export default function PublicHomePage() {
  return (
    <>
      <section className="home-hero">
        <div className="hero-orb hero-orb-one" />
        <div className="hero-orb hero-orb-two" />

        <div className="container home-hero-grid">
          <div className="hero-content">
            <div className="hero-eyebrow">
              <span className="hero-live-dot" />
              DatavionOS · AI Operating System for Healthcare
            </div>

            <h1>
              The healthcare operating system
              <span>built around your organization.</span>
            </h1>

            <p>
              DatavionAI connects clinical operations, pharmacy, finance,
              workforce, analytics, and AI inside one modular platform.
              Start with your organization, configure what you need, and
              scale without rebuilding your technology foundation.
            </p>

            <div className="hero-buttons">
              <Button href="/organization/register">
                Register your organization
              </Button>
              <Button href="/features" variant="outline">
                Explore the platform
              </Button>
            </div>

            <div className="hero-metrics" aria-label="Platform principles">
              <div className="metric-card">
                <strong>Organization-led</strong>
                <span>Context shapes the workspace</span>
              </div>
              <div className="metric-card">
                <strong>Plan-aware</strong>
                <span>Capabilities follow entitlements</span>
              </div>
              <div className="metric-card">
                <strong>Role-specific</strong>
                <span>Access follows each user&apos;s role</span>
              </div>
            </div>

            <div className="hero-trust-line">
              Backend-driven · Multi-tenant · Role-aware · Module-aware
            </div>
          </div>

          <div className="hero-product">
            <div className="product-window">
              <div className="product-window-top">
                <div className="product-dots">
                  <span />
                  <span />
                  <span />
                </div>
                <span>Workspace preview</span>
                <span className="product-status">Illustrative</span>
              </div>

              <div className="product-content">
                <div className="product-heading">
                  <div>
                    <small>Organization workspace</small>
                    <h2>Your healthcare organization</h2>
                  </div>
                  <span className="product-avatar">O</span>
                </div>

                <div className="product-stats">
                  <div><small>Organization</small><strong>Configured</strong></div>
                  <div><small>Subscription</small><strong>Plan-aware</strong></div>
                  <div><small>Modules</small><strong>Role-specific</strong></div>
                  <div><small>Access</small><strong>Permission-led</strong></div>
                </div>

                <div className="product-section-label">Your workspace</div>

                <div className="product-modules">
                  {[
                    ["C", "Clinical operations", "Organization module"],
                    ["P", "Pharmacy", "Role-scoped workspace"],
                    ["R", "Revenue cycle", "Entitlement-aware"],
                    ["A", "AI intelligence", "Department-focused"],
                  ].map(([icon, title, detail]) => (
                    <div key={title} className="product-module">
                      <span>{icon}</span>
                      <div>
                        <strong>{title}</strong>
                        <small>{detail}</small>
                      </div>
                      <b>›</b>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="hero-floating-card hero-card-one">
              <small>Organization context</small>
              <strong>Backend-driven</strong>
              <span>Every workspace starts from the real organization.</span>
            </div>

            <div className="hero-floating-card hero-card-two">
              <small>Module access</small>
              <strong>Role + entitlement</strong>
              <span>See what your organization is allowed to use.</span>
            </div>
          </div>
        </div>
      </section>

      <section className="logo-strip">
        <div className="container">
          <div className="logo-strip-label">
            Built for the functions that keep healthcare moving
          </div>

          <div className="logo-strip-items">
            <span>CLINICAL</span>
            <span>PHARMACY</span>
            <span>REVENUE</span>
            <span>WORKFORCE</span>
            <span>ANALYTICS</span>
          </div>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <SectionTitle
            eyebrow="One operating layer"
            title="One platform, many healthcare workflows."
            description="DatavionOS is designed as a shared foundation so each department can get a focused experience without creating another disconnected application."
          />

          <div className="capability-grid">
            {capabilities.map(([number, title, description]) => (
              <article className="capability-card" key={number}>
                <span className="capability-number">{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
                <span className="card-arrow">↗</span>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <div className="split-section">
            <div>
              <SectionTitle
                eyebrow="Organization-first"
                title="The interface follows the organization."
                description="Instead of hardcoding one generic dashboard, DatavionOS is built so organization context, subscription, modules, departments, and roles shape what users see."
              />

              <div className="architecture-points">
                {[
                  ["Organization", "Category, type, size, location, and structure."],
                  ["Subscription", "Commercial entitlement and available capabilities."],
                  ["Modules", "The capabilities the organization chooses to activate."],
                  ["Roles", "The access boundaries for each user."],
                ].map(([title, description]) => (
                  <div key={title} className="architecture-point">
                    <span>✓</span>
                    <div>
                      <strong>{title}</strong>
                      <p>{description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="architecture-visual">
              <div className="architecture-layer architecture-layer-top">
                <span>ROLE</span>
                <strong>Permissions</strong>
              </div>
              <div className="architecture-layer">
                <span>MODULE</span>
                <strong>Enabled capabilities</strong>
              </div>
              <div className="architecture-layer">
                <span>PLAN</span>
                <strong>Subscription entitlements</strong>
              </div>
              <div className="architecture-layer architecture-layer-bottom">
                <span>ORG</span>
                <strong>Your organization</strong>
              </div>
              <div className="architecture-core">DATAVIONOS</div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <SectionTitle
            eyebrow="How it works"
            title="From registration to a personalized workspace."
            description="The journey starts with your organization and turns into a configured operating environment."
          />

          <div className="journey-grid">
            {journey.map(([number, title, description]) => (
              <article className="journey-card" key={number}>
                <span>{number}</span>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-dark">
        <div className="container">
          <div className="dark-panel">
            <div>
              <div className="section-eyebrow section-eyebrow-light">
                Department intelligence
              </div>
              <h2>AI should belong where the work belongs.</h2>
              <p>
                Pharmacy AI can stay inside pharmacy. Revenue intelligence
                can stay inside finance. Clinical tools can stay inside
                clinical operations. DatavionOS gives the organization a
                common platform without making every user navigate every
                capability.
              </p>
            </div>

            <div className="department-stack">
              <div><span>PHARMACY</span><strong>Pharmacy AI</strong></div>
              <div><span>REVENUE</span><strong>Revenue intelligence</strong></div>
              <div><span>CLINICAL</span><strong>Clinical intelligence</strong></div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="testimonial-layout">
            <div>
              <SectionTitle
                eyebrow="Designed for teams"
                title="Different departments. One operating foundation."
                description="Teams can work in focused spaces while leadership keeps a connected view of the organization."
              />
            </div>

            <div className="testimonial-quote">
              <span>“</span>
              <blockquote>
                The goal is not to give every user every screen. The goal is
                to give each person the right operating experience inside one
                connected organization.
              </blockquote>
              <div>
                <strong>DatavionOS product principle</strong>
                <small>Organization-first architecture</small>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <div className="final-cta">
            <div className="section-eyebrow section-eyebrow-light">
              Start with your organization
            </div>

            <h2>
              Build the healthcare workspace your organization actually needs.
            </h2>

            <p>
              Register your organization to begin the onboarding journey, or
              log in if you already have an account.
            </p>

            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">
                Register organization
              </Button>
              <Button href="/login" variant="outline-light">
                Log in
              </Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
