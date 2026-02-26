import { useState, useEffect, useRef } from "react";
import "../styles/dashboard.css";
import heroBg from "../assets/dash-bg.jpg";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [selectedExperience, setSelectedExperience] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");
  const [previewFile, setPreviewFile] = useState(null);
  const [animatedCount, setAnimatedCount] = useState(0);
  const [scrolled, setScrolled] = useState(false);

  const fileInputRef = useRef();

  /* ================= STICKY NAV ================= */
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 40);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  /* ================= ANIMATED COUNTER ================= */
  useEffect(() => {
    let start = 0;
    const end = searchResults.length;
    if (end === 0) return;

    const duration = 600;
    const increment = end / (duration / 16);

    const counter = setInterval(() => {
      start += increment;
      if (start >= end) {
        setAnimatedCount(end);
        clearInterval(counter);
      } else {
        setAnimatedCount(Math.ceil(start));
      }
    }, 16);

    return () => clearInterval(counter);
  }, [searchResults]);

  /* ================= EXPERIENCE MATCH ================= */
  const matchExperience = (resumeExp, selectedRange) => {
    if (!selectedRange) return true;
    const [min, max] = selectedRange.split("-").map(Number);
    if (max) return resumeExp >= min && resumeExp < max;
    return resumeExp >= min;
  };

  /* ================= SKILL MATCH ================= */
  const matchSkills = (resumeSkills, inputSkills) => {
    if (inputSkills.length === 0) return true;
    return inputSkills.every((skill) =>
      resumeSkills.includes(skill)
    );
  };

  /* ================= UPLOAD ================= */
  const handleUpload = (e) => {
    const files = Array.from(e.target.files);

    const newResumes = files.map((file, index) => ({
      user_id: Date.now() + index,
      name: file.name.replace(".pdf", ""),
      email: `${file.name.split(".")[0]}@gmail.com`,
      skills: ["react", "node"], // simulated skills
      experience: Math.floor(Math.random() * 10) + 1,
      match_score: Math.floor(Math.random() * 40) + 60,
      fileURL: URL.createObjectURL(file),
    }));

    setUploadedFiles((prev) => [...prev, ...newResumes]);
  };

  /* ================= SEARCH ================= */
  const handleSearch = () => {
    if (uploadedFiles.length === 0) {
      setSearchResults([]);
      setSearchMessage("No resumes uploaded yet.");
      return;
    }

    const inputSkills = query
      .toLowerCase()
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    const filtered = uploadedFiles.filter((resume) => {
      const skillMatch = matchSkills(resume.skills, inputSkills);
      const experienceMatch = matchExperience(
        resume.experience,
        selectedExperience
      );

      if (inputSkills.length > 0 && selectedExperience)
        return skillMatch && experienceMatch;

      if (inputSkills.length > 0) return skillMatch;

      if (selectedExperience) return experienceMatch;

      return false;
    });

    if (filtered.length === 0) {
      setSearchResults([]);
      setSearchMessage("No matching results found.");
    } else {
      setSearchResults(filtered);
      setSearchMessage("");
    }
  };

  return (
    <div className="dashboard-wrapper">

      {/* ================= NAVBAR ================= */}
      <nav className={`floating-nav ${scrolled ? "nav-scrolled" : ""}`}>
        <div className="nav-brand">LEXIHIRE</div>

        <div className="nav-links">
          <button>Dashboard</button>

          <button onClick={() => fileInputRef.current.click()}>
            Upload
          </button>

          <button onClick={() => (window.location.href = "/login")}>
            Logout
          </button>
        </div>
      </nav>

      {/* Hidden File Input */}
      <input
        type="file"
        accept=".pdf"
        multiple
        hidden
        ref={fileInputRef}
        onChange={handleUpload}
      />

      {/* ================= HERO ================= */}
      <section
        className="dashboard-hero fade-in"
        style={{ backgroundImage: `url(${heroBg})` }}
      >
        <div className="hero-overlay"></div>

        <div className="hero-content">
          <h1>Find the Right Talent Faster</h1>

          <div className="hero-search-card">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. react, node"
            />

            <select
              value={selectedExperience}
              onChange={(e) => setSelectedExperience(e.target.value)}
            >
              <option value="">Experience</option>
              <option value="0-1">0 - 1</option>
              <option value="1-3">1 - 3</option>
              <option value="3-5">3 - 5</option>
              <option value="5-7">5 - 7</option>
            </select>

            <button onClick={handleSearch}>
              Search Candidates
            </button>
          </div>
        </div>
      </section>

      {/* ================= METRICS ================= */}
      <section className="metrics-section fade-up">
        <div className="metric-card">
          <h4>Total Matches</h4>
          <p>{animatedCount}</p>
        </div>
      </section>

      {/* ================= RESULTS ================= */}
      <section className="results-section fade-up">
        {searchMessage && (
          <div className="empty-state">
            <h3>{searchMessage}</h3>
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="results-container">
            <h3>Matched Resumes</h3>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Experience</th>
                  <th>Match %</th>
                  <th>View</th>
                  <th>Download</th>
                </tr>
              </thead>
              <tbody>
                {searchResults.map((resume) => (
                  <tr key={resume.user_id}>
                    <td>{resume.name}</td>
                    <td>{resume.email}</td>
                    <td>{resume.experience} yrs</td>
                    <td>{resume.match_score}%</td>
                    <td>
                      <button
                        onClick={() => setPreviewFile(resume.fileURL)}
                      >
                        View
                      </button>
                    </td>
                    <td>
                      <a href={resume.fileURL} download>
                        ⬇
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* ================= MODAL ================= */}
      {previewFile && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button
              className="close-btn"
              onClick={() => setPreviewFile(null)}
            >
              ✖
            </button>
            <iframe src={previewFile} title="Resume Preview" />
          </div>
        </div>
      )}
    </div>
  );
}