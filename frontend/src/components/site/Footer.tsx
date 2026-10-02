import Link from "next/link";

const groups = [
  {
    title: "Product",
    links: [
      ["/features", "Platform"],
      ["/solutions", "Solutions"],
      ["/pricing", "Pricing"],
      ["/case-studies", "Case studies"],
    ],
  },
  {
    title: "Company",
    links: [
      ["/about", "About"],
      ["/careers", "Careers"],
      ["/support", "Support"],
    ],
  },
  {
    title: "Account",
    links: [
      ["/login", "Log in"],
      ["/organization/register", "Register organization"],
    ],
  },
];

export function Footer() {
  return (
    <footer className="site-footer">
      <div className="container">
        <div className="footer-grid">
          <div className="footer-intro">
            <Link href="/" className="site-brand footer-brand">
              <span className="site-brand-mark">D</span>
              <span className="site-brand-name">
                Datavion<span>AI</span>
              </span>
            </Link>

            <p>
              DatavionOS is the AI operating system for healthcare:
              one modular foundation for clinical, operational, financial,
              and intelligent workflows.
            </p>

            <div className="footer-badges">
              <span>AI-native</span>
              <span>Multi-tenant</span>
              <span>Enterprise-ready</span>
            </div>
          </div>

          {groups.map((group) => (
            <div className="footer-group" key={group.title}>
              <h2>{group.title}</h2>

              {group.links.map(([href, label]) => (
                <Link href={href} key={href}>
                  {label}
                </Link>
              ))}
            </div>
          ))}

          <div className="footer-cta">
            <h2>Build around your organization.</h2>
            <p>
              Start with organization registration and let DatavionOS become
              the operating layer for your teams.
            </p>

            <Link
              href="/organization/register"
              className="site-button site-button-light"
            >
              Get started
            </Link>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} DatavionAI. All rights reserved.</span>
          <span>DatavionOS — The AI Operating System for Healthcare</span>
        </div>
      </div>
    </footer>
  );
}
