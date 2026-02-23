import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import Navbar from "../components/Navbar";
import "../styles/home.css";
import Lottie from "lottie-react";

import hiringWorkflowAnimation from "../assets/hiring-workflow.json";
import profileCardAnimation from "../assets/ProfileUserCard.json";

export default function Home() {
  return (
    <>
      <Navbar />

      {/* ================= HERO SECTION ================= */}

      <section className="hero-modern">
        <div className="hero-container">

          <motion.div
            className="hero-left"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="hero-badge-modern">
              AI Powered Resume Intelligence
            </div>

            <h1>
              Find the Right Talent <br />
              <span>Faster & Smarter</span>
            </h1>

            <p>
              Transform resume screening with AI-driven ranking,
              structured filtering, and enterprise-ready workflows.
            </p>

            <div className="hero-buttons">
              <Link to="/login" className="btn-primary-modern">
                Get Started
              </Link>

              <Link to="/how-it-works" className="btn-secondary-modern">
                See How It Works
              </Link>
            </div>
          </motion.div>

          <motion.div
            className="hero-search-card"
            initial={{ opacity: 0, y: 60 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
          >
            <h3>Quick Candidate Search</h3>

            <input
              type="text"
              placeholder="e.g. 5 years React + Node"
            />

            <select>
              <option>Experience Level</option>
              <option>0-2 Years</option>
              <option>3-5 Years</option>
              <option>5+ Years</option>
            </select>

            <button className="search-btn-modern">
              Search Candidates
            </button>
          </motion.div>

        </div>
      </section>

      {/* ================= AI ENGINE SECTION ================= */}

      <section className="workflow-animated-section section-white">

        <div className="workflow-animated-container">

          <div className="workflow-text">
            <h2>
              AI Powered <span>Recruitment Engine</span>
            </h2>

            <p>
              Automate resume parsing, skill extraction and candidate ranking
              using advanced NLP models built for modern HR teams.
            </p>

            <ul>
              <li>✔ Resume Upload & Parsing</li>
              <li>✔ Smart Skill Extraction</li>
              <li>✔ AI-Based Ranking</li>
              <li>✔ Instant Shortlisting</li>
            </ul>
          </div>

          <div className="workflow-animation">
            <Lottie
              animationData={hiringWorkflowAnimation}
              loop
              style={{ height: 420 }}
            />
          </div>

        </div>

      </section>

      {/* ================= CANDIDATE PROFILES SECTION ================= */}

      <section className="candidate-preview-section section-blue">

        <div className="candidate-preview-container">

          <div className="candidate-animation">
            <Lottie
              animationData={profileCardAnimation}
              loop
              style={{ height: 420 }}
            />
          </div>

          <div className="candidate-text">
            <h2>
              Structured <span>Candidate Profiles</span>
            </h2>

            <p>
              Every resume is converted into a structured candidate card,
              making it easy for HR teams to compare, filter and shortlist instantly.
            </p>

            <Link to="/login" className="btn-primary-modern">
              Start Screening
            </Link>
          </div>

        </div>

      </section>

      {/* ================= FEATURES SECTION ================= */}

      <section className="feature-preview section-white">

        <div className="feature-container">

          <div className="feature-text">
            <h2>
              Built for Modern <span>HR Teams</span>
            </h2>

            <p>
              From intelligent parsing to ranked search results,
              LexiHire streamlines every step of your hiring workflow.
            </p>
          </div>

          <div className="feature-cards">
            <div className="feature-card">
              🔍 Ranked Resume Search
            </div>

            <div className="feature-card">
              📊 AI Skill Extraction
            </div>

            <div className="feature-card">
              🔐 Secure Role Access
            </div>

            <div className="feature-card">
              ⚡ Fast Shortlisting
            </div>
          </div>

        </div>

      </section>
      <section className="trusted-section section-white">
  <div className="trusted-container">
    <p className="trusted-label">
      Trusted by modern HR teams
    </p>

    <div className="trusted-logos">
      <div>ACME Corp</div>
      <div>GlobalTech</div>
      <div>HireSphere</div>
      <div>TalentGrid</div>
      <div>WorkNova</div>
    </div>
  </div>
</section>
<section className="metrics-section section-blue">
  <div className="metrics-container">

    <div className="metric-item">
      <h3>10K+</h3>
      <p>Resumes Processed</p>
    </div>

    <div className="metric-item">
      <h3>95%</h3>
      <p>Matching Accuracy</p>
    </div>

    <div className="metric-item">
      <h3>60%</h3>
      <p>Faster Shortlisting</p>
    </div>

  </div>
</section>
<section className="cta-section">
  <div className="cta-container">
    <h2>
      Ready to Transform <span>Your Hiring?</span>
    </h2>

    <p>
      Start using AI-powered resume intelligence today.
    </p>

    <Link to="/login" className="btn-primary-modern">
      Get Started Now
    </Link>
  </div>
</section>


      {/* ================= FOOTER ================= */}

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>

    </>
  );
}
