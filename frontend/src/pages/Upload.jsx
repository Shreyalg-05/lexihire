import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/dashboard.css";
import heroBg from "../assets/dash-bg.jpg";

export default function Upload() {

  const navigate = useNavigate();
  const { logout } = useAuth();
  const fileInputRef = useRef(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFileSelect = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {

    const file = e.target.files[0];

    if (!file) return;

    const formData = new FormData();
    formData.append("resume", file);

    try {

      setLoading(true);
      setError("");
      setResult(null);

      const response = await fetch(
        "http://localhost:5000/resume/upload",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      setLoading(false);

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || "Upload failed.");
      }

    } catch (err) {
      setLoading(false);
      setError("Server error.");
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (

    <div className="dashboard-wrapper">

      {/* NAVBAR */}

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


      {/* HERO */}

      <section
        className="dashboard-hero"
        style={{ backgroundImage: `url(${heroBg})` }}
      >

        <div className="hero-overlay"></div>

        <div className="hero-content">

          <h1>Upload Candidate Resumes</h1>

          <div className="hero-search-card">

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.doc,.docx"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />

            {!loading && !result && (

              <button onClick={handleFileSelect}>
                Upload Resume
              </button>

            )}

            {loading && (

              <div className="upload-loading">
                <div className="loader"></div>
                <p>Parsing resume...</p>
              </div>

            )}

            {result && (

              <div className="upload-success-card">

                <div className="success-check">✔</div>

                <h3>Resume Parsed Successfully</h3>

                <div className="parsed-info">

                  <p>
                    <strong>Candidate ID:</strong> {result.user_id}
                  </p>

                  <p>
                    <strong>Resume:</strong> {result.resume_filename}
                  </p>

                </div>

                <button
                  className="view-dashboard-btn"
                  onClick={() => navigate("/dashboard")}
                >
                  View Candidates
                </button>

              </div>

            )}

            {error && (
              <p className="upload-error">
                {error}
              </p>
            )}

          </div>

        </div>

      </section>

    </div>
  );
}