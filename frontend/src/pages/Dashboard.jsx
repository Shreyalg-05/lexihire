import { useState } from "react";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [activePage, setActivePage] = useState("dashboard");
  const [query, setQuery] = useState("");
  const [selectedExperience, setSelectedExperience] = useState("");

  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");

  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [previewFile, setPreviewFile] = useState(null);

  /* ================= SEARCH ================= */
  const handleSearch = () => {
    const trimmedQuery = query.toLowerCase().trim();

    if (uploadedFiles.length === 0) {
      setSearchResults([]);
      setSearchMessage("No resumes uploaded yet.");
      return;
    }

    // Convert comma-separated skills properly
    const skillKeywords = trimmedQuery
      ? trimmedQuery
          .split(",")
          .map((s) => s.trim())
          .filter((s) => s.length > 0)
      : [];

    // Demo Resume Data
    const enrichedResumes = uploadedFiles.map((file, index) => ({
      id: index + 1,
      name: "Candidate " + (index + 1),
      email: "candidate" + (index + 1) + "@example.com",
      skills: ["java", "react", "node.js", "sql", "spring boot"],
      experience: 5, // numeric value
      match: "85%",
      url: file.url,
    }));

    const matched = enrichedResumes.filter((resume) => {
      let skillMatch = true;
      let experienceMatch = true;

      /* ===== SKILL FILTER ===== */
      if (skillKeywords.length > 0) {
        const resumeSkillsLower = resume.skills.map((skill) =>
          skill.toLowerCase()
        );

        // OR logic (any keyword matches)
        skillMatch = skillKeywords.some((keyword) =>
          resumeSkillsLower.some((skill) =>
            skill.includes(keyword)
          )
        );
      }

      /* ===== EXPERIENCE FILTER ===== */
      if (selectedExperience) {
        const [minExp, maxExp] = selectedExperience
          .split("-")
          .map(Number);

        if (maxExp === 20) {
          // last range inclusive
          experienceMatch =
            resume.experience >= minExp &&
            resume.experience <= maxExp;
        } else {
          // exclusive upper bound (prevents overlap)
          experienceMatch =
            resume.experience >= minExp &&
            resume.experience < maxExp;
        }
      }

      return skillMatch && experienceMatch;
    });

    if (matched.length > 0) {
      setSearchResults(matched);
      setSearchMessage("");
    } else {
      setSearchResults([]);
      setSearchMessage("No matching results found.");
    }
  };

  /* ================= FILE UPLOAD ================= */
  const handleFileUpload = (e) => {
    const files = Array.from(e.target.files).map((file) => ({
      name: file.name,
      url: URL.createObjectURL(file),
    }));

    setUploadedFiles((prev) => [...prev, ...files]);
  };

  const deleteFile = (index) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="dashboard-body">
      <header className="top-header">
        <h1 className="brand-title">LEXIHIRE</h1>

        <div className="top-nav">
          <button
            className={activePage === "dashboard" ? "nav-btn active" : "nav-btn"}
            onClick={() => {
              setActivePage("dashboard");
              setSearchResults([]);
              setSearchMessage("");
            }}
          >
            Dashboard
          </button>

          <button
            className={activePage === "upload" ? "nav-btn active" : "nav-btn"}
            onClick={() => setActivePage("upload")}
          >
            Upload Resumes
          </button>

          <button
            className="nav-btn"
            onClick={() => {
              localStorage.removeItem("isAuthenticated");
              window.location.href = "/login";
            }}
          >
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        <div className="dashboard-stats">
          <div className="stat-card">
            <h4>Total Resumes</h4>
            <p>{uploadedFiles.length}</p>
          </div>

          <div className="stat-card">
            <h4>Last Search</h4>
            <p>{query || "—"}</p>
          </div>

          <div className="stat-card">
            <h4>Matches Found</h4>
            <p>{searchResults.length}</p>
          </div>
        </div>

        {activePage === "dashboard" && (
          <>
            <div className="query-box">
              <p className="query-hint">👋 Enter your hiring requirement</p>

              <div className="query-input">
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  placeholder="Type skills (comma separated)"
                />

                <select
                  className="experience-dropdown"
                  value={selectedExperience}
                  onChange={(e) => setSelectedExperience(e.target.value)}
                >
                  <option value="">Experience</option>
                  <option value="0-1">0 - 1 years</option>
                  <option value="1-2">1 - 2 years</option>
                  <option value="2-3">2 - 3 years</option>
                  <option value="3-5">3 - 5 years</option>
                  <option value="5-7">5 - 7 years</option>
                  <option value="7-10">7 - 10 years</option>
                  <option value="10-15">10 - 15 years</option>
                  <option value="15-20">15 - 20 years</option>
                </select>

                <button onClick={handleSearch}>Search</button>
              </div>
            </div>

            {searchMessage && (
              <div className="empty-state">
                <h3>{searchMessage}</h3>
                <p>Try refining your search or upload resumes first.</p>
              </div>
            )}

            {searchResults.length > 0 && (
              <div className="results">
                <h3 className="table-title">Shortlisted Candidates</h3>

                <table className="compact-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Match %</th>
                      <th>Resume</th>
                      <th>Download</th>
                    </tr>
                  </thead>

                  <tbody>
                    {searchResults.map((resume) => (
                      <tr key={resume.id}>
                        <td>{resume.id}</td>
                        <td>{resume.name}</td>
                        <td>{resume.email}</td>
                        <td>{resume.match}</td>
                        <td>
                          <button
                            className="view-btn"
                            onClick={() => setPreviewFile(resume.url)}
                          >
                            View
                          </button>
                        </td>
                        <td>
                          <a href={resume.url} download>
                            ⬇
                          </a>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        {activePage === "upload" && (
          <div className="upload-section">
            <input
              type="file"
              accept=".pdf"
              multiple
              hidden
              id="uploadInput"
              onChange={handleFileUpload}
            />

            <label htmlFor="uploadInput" className="upload-btn">
              📄 Upload Resumes
            </label>

            {uploadedFiles.length === 0 ? (
              <h2 className="upload-empty">No resumes uploaded yet !!</h2>
            ) : (
              <div className="table-wrapper">
                <h3 className="table-title-left">Uploaded Resumes</h3>

                <table className="upload-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>File Name</th>
                      <th>View</th>
                      <th>Delete</th>
                    </tr>
                  </thead>
                  <tbody>
                    {uploadedFiles.map((file, index) => (
                      <tr key={index}>
                        <td>{index + 1}</td>
                        <td>{file.name}</td>
                        <td>
                          <button
                            className="view-btn"
                            onClick={() => setPreviewFile(file.url)}
                          >
                            View
                          </button>
                        </td>
                        <td>
                          <button
                            className="icon-btn"
                            onClick={() => deleteFile(index)}
                          >
                            🗑
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </main>

      {previewFile && (
        <div className="modal-overlay">
          <div className="modal-content large-preview">
            <div className="modal-header">
              <span>Resume Preview</span>
              <button onClick={() => setPreviewFile(null)}>✖</button>
            </div>

            <iframe
              src={previewFile}
              title="Resume Preview"
              className="resume-frame"
            />
          </div>
        </div>
      )}
    </div>
  );
}
