import { useState } from "react";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [activePage, setActivePage] = useState("dashboard");
  const [query, setQuery] = useState("");
  const [selectedExperience, setSelectedExperience] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");
  const [previewFile, setPreviewFile] = useState(null);

  /* ================= SEARCH ================= */
  const handleSearch = async () => {
    try {
      let url = "http://127.0.0.1:5000/search?";

      if (query) {
        url += `skills=${encodeURIComponent(query)}&`;
      }

      if (selectedExperience) {
        url += `experience=${selectedExperience}&`;
      }

      const response = await fetch(url);
      const data = await response.json();

      if (response.ok) {
        setSearchResults(data);
        setSearchMessage(
          data.length === 0 ? "No matching results found." : ""
        );
      } else {
        setSearchResults([]);
        setSearchMessage("Search failed.");
      }
    } catch (error) {
      console.error(error);
      setSearchMessage("Server error.");
    }
  };

  /* ================= FILE UPLOAD ================= */
  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    const formData = new FormData();

    files.forEach((file) => {
      formData.append("resume", file);
    });

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/resume/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        alert("Upload successful!");
      } else {
        alert("Upload failed");
      }
    } catch (error) {
      console.error(error);
      alert("Server error");
    }
  };

  return (
    <div className="dashboard-body">
      <header className="top-header">
        <h1 className="brand-title">LEXIHIRE</h1>

        <div className="top-nav">
          <button
            className={
              activePage === "dashboard"
                ? "nav-btn active"
                : "nav-btn"
            }
            onClick={() => {
              setActivePage("dashboard");
              setSearchResults([]);
              setSearchMessage("");
            }}
          >
            Dashboard
          </button>

          <button
            className={
              activePage === "upload"
                ? "nav-btn active"
                : "nav-btn"
            }
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
        {/* ================= STATS ================= */}
        <div className="dashboard-stats">
          <div className="stat-card">
            <h4>Last Search</h4>
            <p>{query || "—"}</p>
          </div>

          <div className="stat-card">
            <h4>Matches Found</h4>
            <p>{searchResults.length}</p>
          </div>
        </div>

        {/* ================= DASHBOARD PAGE ================= */}
        {activePage === "dashboard" && (
          <>
            <div className="query-box">
              <p className="query-hint">
                👋 Enter your hiring requirement
              </p>

              <div className="query-input">
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) =>
                    e.key === "Enter" && handleSearch()
                  }
                  placeholder="Type skills (comma separated)"
                />

                <select
                  className="experience-dropdown"
                  value={selectedExperience}
                  onChange={(e) =>
                    setSelectedExperience(e.target.value)
                  }
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

                <button onClick={handleSearch}>
                  Search
                </button>
              </div>
            </div>

            {searchMessage && (
              <div className="empty-state">
                <h3>{searchMessage}</h3>
              </div>
            )}

            {searchResults.length > 0 && (
              <div className="results">
                <h3 className="table-title">
                  Matched Resumes
                </h3>

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
                      <tr key={resume.user_id}>
                        <td>{resume.user_id}</td>
                        <td>{resume.name}</td>
                        <td>{resume.email}</td>
                        <td>{resume.match_score}%</td>

                        {/* VIEW IN SAME PAGE */}
                        <td>
                          <button
                            className="view-btn"
                            onClick={() =>
                              setPreviewFile(
                                `http://127.0.0.1:5000/resume/view/${resume.user_id}/${resume.resume_url}`
                              )
                            }
                          >
                            View
                          </button>
                        </td>

                        {/* FORCE DOWNLOAD */}
                        <td>
                          <a
                            href={`http://127.0.0.1:5000/resume/download/${resume.user_id}/${resume.resume_url}`}
                          >
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

        {/* ================= UPLOAD PAGE ================= */}
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
            <label
              htmlFor="uploadInput"
              className="upload-btn"
            >
              📄 Upload Resumes
            </label>
          </div>
        )}
      </main>

      {/* ================= MODAL ================= */}
      {previewFile && (
        <div className="modal-overlay">
          <div className="modal-content large-preview">
            <div className="modal-header">
              <span>Resume Preview</span>
              <button onClick={() => setPreviewFile(null)}>
                ✖
              </button>
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
