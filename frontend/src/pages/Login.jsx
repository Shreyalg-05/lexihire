import { useState } from "react";
import "../styles/login.css";
import loginImage from "../assets/login-hr.jpeg";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const validateInputs = () => {
    if (!email || !password) return "Email and password are required";
    if (!email.includes("@")) return "Enter a valid email address";
    if (password.length < 6) return "Password must be at least 6 characters";
    return null;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    const validationError = validateInputs();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    setTimeout(() => {
      const storedPassword =
        localStorage.getItem("adminPassword") || "admin123";

      if (
        email === "admin@lexihire.com" &&
        password === storedPassword
      ) {
        localStorage.setItem("isAuthenticated", "true");
        window.location.href = "/dashboard";
      } else {
        setError("Invalid email or password");
      }

      setLoading(false);
    }, 800);
  };

  return (
    <div className="login-page">
      <div className="login-container">

        {/* LEFT PANEL WITH IMAGE */}
        <div
          className="login-left-image"
          style={{ backgroundImage: `url(${loginImage})` }}
        >
          <div className="image-overlay"></div>
          <div className="image-text">
            <h1>Resume Shortlisting</h1>
            <p>
              Upload resumes, search using natural language,
              and hire faster with confidence.
            </p>
          </div>
        </div>

        {/* RIGHT PANEL FORM */}
        <div className="login-right">
          <div className="login-form-card">
            <h2>Welcome Back</h2>
            <p>Sign in to access your HR dashboard</p>

            <form onSubmit={handleSubmit}>
              <input
                type="email"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <div className="password-wrapper">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>

              {error && <div className="login-error">{error}</div>}

              <div className="forgot">
                <a href="/reset-password">Forgot password?</a>
              </div>

              <button type="submit" className="login-btn">
                {loading ? "Signing in..." : "Login"}
              </button>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}
