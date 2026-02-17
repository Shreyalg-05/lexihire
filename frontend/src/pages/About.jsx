import Navbar from "../components/Navbar";
import "../styles/home.css";

export default function About() {
  return (
    <>
      <Navbar />

      {/* ================= ABOUT HEADER ================= */}
      <section className="about-hero">
        <div className="about-hero-inner">
          <h1>About LexiHire</h1>
          <p>
            A role-based resume processing and hiring system built for
            organizations managing large volumes of candidate applications.
          </p>
        </div>
      </section>

      {/* ================= ABOUT CONTENT ================= */}
      <section className="about-content">
        <div className="about-container">
          <h3>What LexiHire Does</h3>
          <p>
            LexiHire enables candidates to securely upload resumes while HR teams
            search, rank, shortlist, and download resumes using natural language
            queries. The system is designed to reduce manual screening effort and
            improve consistency in candidate evaluation.
          </p>

          <h3>Designed for Enterprise Workflows</h3>
          <p>
            The platform enforces clear role separation between candidates and
            hiring teams, ensuring that access to data and actions is controlled
            and auditable. All resume interactions are tracked to support
            accountability and compliance requirements.
          </p>

          <h3>Focus on Transparency and Control</h3>
          <p>
            LexiHire provides transparent, ranked search results to help hiring
            teams understand why candidates surface for specific queries. This
            approach supports fairer decision-making and improves trust in the
            shortlisting process.
          </p>
          <h3>Core Principles</h3>
            <ul className="about-list">
             <li>Role-based access control for candidates and HR teams</li>
             <li>Audit-friendly workflows with traceable actions</li>
             <li>Transparent, ranked resume search results</li>
             <li>Designed for high-volume, enterprise hiring pipelines</li>
            </ul>
        </div>
      </section>

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>
    </>
  );
}
