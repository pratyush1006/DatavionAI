import { Button } from "@/components/site/Button";
import { SectionTitle } from "@/components/site/SectionTitle";

const plans = [
  {
    name: "Launch",
    description: "For organizations building a focused digital operating foundation.",
    price: "Custom",
    featured: false,
    points: [
      "Core organization workspace",
      "Essential operational capabilities",
      "Role-based access",
      "Standard support",
    ],
  },
  {
    name: "Scale",
    description: "For growing organizations with broader department requirements.",
    price: "Custom",
    featured: true,
    points: [
      "Everything in Launch",
      "Expanded department capabilities",
      "Advanced analytics",
      "AI capabilities",
      "Organization module controls",
    ],
  },
  {
    name: "Enterprise",
    description: "For complex organizations with broad operational requirements.",
    price: "Talk to us",
    featured: false,
    points: [
      "Enterprise operating model",
      "Advanced access controls",
      "Multi-organization scenarios",
      "Integration pathways",
      "Enterprise support",
    ],
  },
];

export default function PricingPage() {
  return (
    <>
      <section className="page-hero">
        <div className="container narrow">
          <div className="section-eyebrow">Pricing</div>
          <h1>Choose a commercial tier. Configure the workspace from there.</h1>
          <p>
            Subscription defines the commercial capability envelope. Your
            organization then configures the modules and access patterns inside
            that envelope.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="container">
          <div className="pricing-grid">
            {plans.map((plan) => (
              <article
                className={`pricing-card ${plan.featured ? "is-featured" : ""}`}
                key={plan.name}
              >
                {plan.featured ? <span className="pricing-badge">Most popular</span> : null}

                <span className="pricing-eyebrow">{plan.name}</span>
                <h2>{plan.description}</h2>
                <div className="pricing-price">{plan.price}</div>
                <small>Contact DatavionAI for your organization.</small>

                <div className="pricing-divider" />

                {plan.points.map((point) => (
                  <div className="pricing-point" key={point}>
                    <span>✓</span>
                    <p>{point}</p>
                  </div>
                ))}

                <div className="pricing-action">
                  <Button href="/organization/register">
                    Start with {plan.name}
                  </Button>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section-block section-muted">
        <div className="container">
          <SectionTitle
            eyebrow="Pricing model"
            title="Subscription is the beginning—not the whole experience."
            description="The target product model connects commercial entitlement to organization context, module activation, and role-based access."
          />

          <div className="architecture-wide">
            {[
              ["SUBSCRIPTION", "Commercial capability envelope"],
              ["ORGANIZATION", "Healthcare context"],
              ["MODULES", "Capabilities enabled"],
              ["ROLES", "Access boundaries"],
            ].map(([title, description]) => (
              <div className="architecture-wide-card" key={title}>
                <span>→</span>
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
            <div className="section-eyebrow section-eyebrow-light">Get started</div>
            <h2>Start with the organization, not the menu.</h2>
            <p>Register your organization and let onboarding establish the workspace context.</p>
            <div className="hero-buttons">
              <Button href="/organization/register" variant="light">Register organization</Button>
              <Button href="/support" variant="outline-light">Talk to support</Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
