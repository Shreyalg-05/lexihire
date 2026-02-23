import Navbar from "../components/Navbar";
import { motion } from "framer-motion";
import "../styles/home.css";
import aboutBg from "../assets/about-bg.jpeg";

export default function About() {
  return (
    <>
      <Navbar />

      {/* ================= HERO ================= */}

      <section
        className="about-hero"
        style={{ backgroundImage: `url(${aboutBg})` }}
      >
        <div className="about-hero-overlay"></div>

        <div className="about-hero-content">
          <h1>
            Building the Future of <span>AI Hiring</span>
          </h1>
          <p>
            LexiHire transforms resume screening into a transparent,
            structured and intelligent hiring experience.
          </p>
        </div>
      </section>

      {/* ================= MISSION ================= */}

      <section className="about-section about-light">

        <div className="about-container">

          <motion.div
            className="about-text-block"
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            viewport={{ once: true }}
          >
            <h2>Our Mission</h2>
            <p>
              Reduce manual screening effort while improving fairness,
              transparency and scalability in enterprise hiring.
            </p>
          </motion.div>

        </div>
      </section>

      {/* ================= WHY LEXIHIRE ================= */}

      <section className="about-section about-gradient">

        <div className="about-container grid-2">

          <div>
            <h2>Why LexiHire?</h2>
            <p>
              Traditional resume screening is manual, inconsistent,
              and difficult to scale. LexiHire uses AI-driven ranking,
              structured workflows and audit-friendly systems
              to modernize enterprise recruitment.
            </p>
          </div>

          <div className="about-highlight-card">
            <h3>Designed for HR Teams</h3>
            <ul>
              <li>Structured candidate scoring</li>
              <li>Natural language search</li>
              <li>Secure role-based access</li>
              <li>Enterprise-level scalability</li>
            </ul>
          </div>

        </div>

      </section>

      {/* ================= PRINCIPLES ================= */}

      <section className="about-section about-light">

        <div className="about-container grid-3">

          {[
            ["🔐", "Security First"],
            ["⚙️", "Structured Workflows"],
            ["📊", "Transparent Ranking"]
          ].map((item, index) => (
            <motion.div
              key={index}
              className="about-mini-card"
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              viewport={{ once: true }}
            >
              <div className="about-icon">{item[0]}</div>
              <h4>{item[1]}</h4>
            </motion.div>
          ))}

        </div>

      </section>

      {/* ================= STATS ================= */}

      <section className="about-section about-dark">

        <div className="about-container grid-3 center-text">

          <div>
            <h2>10K+</h2>
            <p>Resumes Processed</p>
          </div>

          <div>
            <h2>95%</h2>
            <p>Search Accuracy</p>
          </div>

          <div>
            <h2>50+</h2>
            <p>Enterprise Clients</p>
          </div>

        </div>

      </section>

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>
    </>
  );
}
