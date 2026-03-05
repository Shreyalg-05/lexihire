import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/dashboard.css";
import heroBg from "../assets/dash-bg.jpg";

export default function Dashboard() {

  const navigate = useNavigate();
  const { logout } = useAuth();

  const [query, setQuery] = useState("");
  const [selectedExperience, setSelectedExperience] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchMessage, setSearchMessage] = useState("");
  const [previewFile, setPreviewFile] = useState(null);

  const handleSearch = async () => {

    if (query === "" && selectedExperience === "") {
      setSearchMessage("Enter skills or experience to search.");
      return;
    }

    try {

      let url = "http://localhost:5000/search?";

      if (query) {
        url += `skills=${encodeURIComponent(query)}&`;
      }

      if (selectedExperience) {
        url += `experience=${selectedExperience}&`;
      }

      const response = await fetch(url);

      const data = await response.json();

      if (data.length === 0) {
        setSearchResults([]);
        setSearchMessage("No matching results found.");
        return;
      }

      setSearchResults(data);
      setSearchMessage("");

    } catch (error) {
      console.error(error);
      setSearchMessage("Server error.");
    }
  };

    const dummyResults = [
      {
        user_id: 1,
        name: "Candidate 1",
        email: "candidate1@gmail.com",
        skills: ["react", "node"],
        experience: 4,
        fileURL: "/sample-resume.pdf"
      },
      {
        user_id: 2,
        name: "Candidate 2",
        email: "candidate2@gmail.com",
        skills: ["python", "ml"],
        experience: 5,
        fileURL: "/sample-resume.pdf"
      }
    ];

    setSearchResults(dummyResults);
    setSearchMessage("");
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (

    <div className="dashboard-wrapper">

      <nav className="floating-nav">

        <div className="nav-brand">LEXIHIRE</div>

        <div className="nav-links">

          <button onClick={() => navigate("/dashboard")}>
            Dashboard
          </button>

          <button onClick={() => navigate("/upload")}>
            Upload
          </button>

          <button onClick={handleLogout}>
            Logout
          </button>

        </div>

      </nav>

      <section
        className="dashboard-hero"
        style={{ backgroundImage: `url(${heroBg})` }}
      >

        <div className="hero-overlay"></div>

        <div className="hero-content">

          <h1>Find the Right Talent Faster</h1>

          <div className="hero-search-card">

            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. react, python"
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

      <section className="results-section">

        {searchMessage && (
          <div className="empty-state">
            <h3>{searchMessage}</h3>
          </div>
        )}

        {searchResults.length > 0 && (

          <div className="candidate-layout">

            <div className="candidate-list">

              {searchResults.map((resume) => (

                <div
                  key={resume.user_id}
                  className="candidate-card"
                  onClick={() =>
                    setPreviewFile(
                      `http://localhost:5000/resume/view/${resume.user_id}/${resume.resume_url}`
                    )
                  }
                >

                  <div className="candidate-avatar">
                    {resume.name.charAt(0)}
                  </div>

                  <div className="candidate-info">

                    <h4>{resume.name}</h4>

                    <p>{resume.email}</p>

                    <div className="skill-tags">

                      {resume.skills.slice(0,4).map((skill, index) => (
                        <span key={index}>{skill}</span>
                      ))}

                      {resume.skills.length > 4 && (
                        <span className="more-skills">
                          +{resume.skills.length - 4} more
                        </span>
                      )}

                      </div>

                    <div className="exp">
                      {resume.experience} yrs experience
                    </div>

                    <a
                      href={`http://localhost:5000/resume/download/${resume.user_id}/${resume.resume_url}`}
                      download
                      className="download-btn"
                      onClick={(e)=>e.stopPropagation()}
                    >
                      Download
                    </a>

                  </div>

                </div>

              ))}

            </div>

            <div className="preview-panel">

              {previewFile ? (

                <iframe
                  src={previewFile}
                  title="Resume Preview"
                />

              ) : (

                <div className="preview-placeholder">
                  Select a candidate to preview resume
                </div>

              )}

            </div>

          </div>

        )}

      </section>

    </div>

  );

}