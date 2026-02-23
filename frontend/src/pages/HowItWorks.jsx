import Navbar from "../components/Navbar";
import { motion } from "framer-motion";
import "../styles/home.css";
import talentImage from "../assets/talent-hand.jpeg"; // place image 2 inside assets

export default function HowItWorks() {
  return (
    <>
      <Navbar />

      {/* ================= HERO ================= */}

      <section className="how-hero">

        <div className="how-hero-overlay"></div>

        <div className="how-hero-container">

          <motion.div
            className="how-hero-text"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1>
              Enterprise <span>Hiring Workflow</span>
            </h1>

            <p>
              Secure, structured, and optimized for large-scale recruitment.
            </p>
          </motion.div>

        </div>

      </section>

      {/* ================= WORKFLOW CARDS ================= */}

      <section className="how-workflow-section">

        <div className="how-workflow-container">

          {[
            ["📤", "Secure Resume Upload"],
            ["🧠", "AI Parsing & Indexing"],
            ["🔍", "Ranked Natural Language Search"],
            ["📥", "Shortlist & Download"]
          ].map((item, index) => (
            <motion.div
              className="how-workflow-card"
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              viewport={{ once: true }}
            >
              <div className="how-icon">{item[0]}</div>
              <h3>{item[1]}</h3>
              <p>
                Built for structured enterprise workflows with
                full audit tracking and role separation.
              </p>
            </motion.div>
          ))}

        </div>

      </section>

      {/* ================= TALENT IMAGE SECTION ================= */}

      <section className="how-talent-section">

        <div className="how-talent-container">

          <motion.div
            className="how-talent-text"
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2>
              AI Identifies <span>Top Talent Instantly</span>
            </h2>

            <p>
              Our recruitment engine intelligently evaluates resumes,
              ranks candidates and surfaces the best matches instantly —
              helping HR teams make confident decisions.
            </p>
          </motion.div>

          <motion.div
            className="how-talent-image"
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <img src={talentImage} alt="AI Talent Selection" />
          </motion.div>

        </div>

      </section>

      <footer className="footer">
        © 2026 LexiHire. All rights reserved.
      </footer>
    </>
  );
}
