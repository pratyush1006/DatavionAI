import Link from "next/link";

export default function PublicNotFound() {
  return (
    <section className="page-hero">
      <div className="container narrow">
        <div className="section-eyebrow">404</div>
        <h1>That page is not part of the public DatavionAI site.</h1>
        <p>
          Return home, explore the platform, or start your organization registration.
        </p>
        <div className="hero-buttons">
          <Link href="/" className="site-button site-button-primary">
            Go home
          </Link>
          <Link href="/features" className="site-button site-button-outline">
            Explore platform
          </Link>
        </div>
      </div>
    </section>
  );
}
