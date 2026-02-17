import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "../styles/home.css";

export default function Home() {
  return (
    <>
      <Navbar />

      {/* ================= HERO ================= */}
      <section className="hero-modern">
        <div className="hero-content">
          <h1>
            Intelligent <span>Resume Search</span> <br />
            Built for Modern Hiring
          </h1>

          <p>
            Upload resumes, search using natural language, and
            shortlist candidates instantly with AI-powered ranking.
          </p>

          <div className="hero-buttons">
            <Link to="/login" className="btn-primary">
              Get Started
            </Link>

            <Link to="/about" className="btn-secondary">
              Learn More
            </Link>
          </div>

          <div className="hero-stats">
            <div>
              <h3>10K+</h3>
              <p>Resumes Processed</p>
            </div>
            <div>
              <h3>95%</h3>
              <p>Search Accuracy</p>
            </div>
            <div>
              <h3>50+</h3>
              <p>Enterprise Teams</p>
            </div>
          </div>
        </div>

        {/* RIGHT SIDE MOCK DASHBOARD */}
        <div className="hero-visual">
          <div className="mock-card large">
            <h4>Search Query</h4>
            <p>“5 years Java developer with Spring Boot”</p>
          </div>

          <div className="mock-card small">
            <h4>Top Match</h4>
            <p>John Doe — 85%</p>
          </div>

          <div className="mock-card accent">
            <h4>Shortlisted</h4>
            <p>12 Candidates</p>
          </div>
        </div>
      </section>

      {/* ================= FEATURES ================= */}
      <section className="features-section">
        <h2>Why LexiHire?</h2>

        <div className="features-grid">
          <div className="feature-card">
            <h3>Natural Language Search</h3>
            <p>
              Search resumes using plain English instead of complex filters.
            </p>
          </div>

          <div className="feature-card">
            <h3>Role-Based Access</h3>
            <p>
              Secure workflows for candidates and HR teams.
            </p>
          </div>

          <div className="feature-card">
            <h3>Smart Ranking</h3>
            <p>
              AI-powered relevance scoring to reduce screening time.
            </p>
          </div>

          <div className="feature-card">
            <h3>Audit-Friendly</h3>
            <p>
              Trackable resume interactions for compliance and transparency.
            </p>
          </div>
        </div>
      </section>

      {/* ================= CTA ================= */}
      <section className="cta-section">
        <h2>Transform Your Hiring Workflow</h2>
        <p>Start using LexiHire today and hire faster with confidence.</p>

        <Link to="/login" className="btn-primary">
          Access Dashboard
        </Link>
      </section>

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>
    </>
  );
}
