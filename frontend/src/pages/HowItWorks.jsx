import Navbar from "../components/Navbar";
import "../styles/home.css";

export default function HowItWorks() {
  return (
    <>
      <Navbar />

      <section className="how-hero">
  <div className="how-hero-inner">
    <h1>How LexiHire Works</h1>
    <p>
      A structured, role-based workflow designed for secure,
      high-volume resume processing.
    </p>
  </div>
</section>


      <section className="how-wrapper">
        <div className="how-grid">

          <div className="how-card">
            <span className="step">1</span>
            <div className="icon">📤</div>
            <h3>Resume Upload</h3>
            <p>
              Candidates securely upload resumes in PDF or DOCX format.
              Files are stored with access controls.
            </p>
          </div>

          <div className="how-card">
            <span className="step">2</span>
            <div className="icon">🧠</div>
            <h3>Parsing & Indexing</h3>
            <p>
              Resume content is extracted and indexed automatically
              for efficient search and ranking.
            </p>
          </div>

          <div className="how-card">
            <span className="step">3</span>
            <div className="icon">🔍</div>
            <h3>Natural Language Search</h3>
            <p>
              HR teams search resumes using plain English queries
              and receive ranked results.
            </p>
          </div>

          <div className="how-card">
            <span className="step">4</span>
            <div className="icon">📥</div>
            <h3>Shortlist & Download</h3>
            <p>
              Candidates are shortlisted and resumes are downloaded
              directly from a unified dashboard.
            </p>
          </div>

        </div>
      </section>

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>
    </>
  );
}
