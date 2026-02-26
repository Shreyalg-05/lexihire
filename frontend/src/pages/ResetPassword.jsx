import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";
import bgImage from "../assets/login-bg.jpeg";

export default function ResetPassword() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email.trim()) {
      setMessage("Please enter your registered email.");
      return;
    }

    setLoading(true);
    setMessage("");

    // Simulated API call
    setTimeout(() => {
      setMessage("Reset link sent successfully to your email.");
      setLoading(false);
    }, 1000);
  };

  return (
    <div
      className="login-page"
      style={{ backgroundImage: `url(${bgImage})` }}
    >
      <div className="glass-container">

        {/* ===== Brand (same as login) ===== */}
        <div className="brand">
          <div className="brand-dot"></div>
          <span>LexiHire</span>
        </div>

        <div className="content">
          <div className="login-card">
            <h2>Reset Password</h2>

            <form onSubmit={handleSubmit}>

              {/* Email Input */}
              <input
                type="email"
                placeholder="Enter your registered email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              {/* Success / Error Message */}
              {message && (
                <p className="error-text" style={{ color: "#16a34a" }}>
                  {message}
                </p>
              )}

              {/* Button */}
              <button
                type="submit"
                className="login-btn"
                disabled={loading}
              >
                {loading ? "Sending..." : "Send Reset Link"}
              </button>

            </form>

            {/* Back to Login */}
            <p
              className="register"
              style={{ cursor: "pointer" }}
              onClick={() => navigate("/login")}
            >
              Back to Login
            </p>

          </div>
        </div>

      </div>
    </div>
  );
}