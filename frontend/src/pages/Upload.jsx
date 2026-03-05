import { useState } from "react";
import "../styles/dashboard.css";

export default function Upload() {

  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFiles([...e.target.files]);
  };

  const handleUpload = async () => {

    if (files.length === 0) {
      setMessage("Please select resume files.");
      return;
    }

    const formData = new FormData();

    files.forEach(file => {
      formData.append("resume", file);
    });

    try {

      const response = await fetch(
        "http://localhost:5000/resume/upload",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message);
      } else {
        setMessage(data.error || "Upload failed.");
      }

    } catch (error) {
      console.error(error);
      setMessage("Server error.");
    }
  };

  return (
    <div className="dashboard-wrapper">

      {/* NAVBAR */}

      <nav className="floating-nav">

        <div className="nav-brand">LEXIHIRE</div>

        <div className="nav-links">

          <button onClick={() => window.location.href="/dashboard"}>
            Dashboard
          </button>

          <button onClick={() => window.location.href="/upload"}>
            Upload
          </button>

          <button onClick={() => window.location.href="/login"}>
            Logout
          </button>

        </div>

      </nav>

      {/* UPLOAD SECTION */}

      <section className="results-section">

        <div className="results-container">

          <h3>Upload Resumes</h3>

          <input
            type="file"
            multiple
            accept=".pdf,.doc,.docx"
            onChange={handleFileChange}
          />

          <br /><br />

          <button onClick={handleUpload}>
            Upload Resume
          </button>

          {message && (
            <p style={{marginTop:"20px"}}>
              {message}
            </p>
          )}

        </div>

      </section>

    </div>
  );
}