import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useState, useEffect } from "react";
import { Eye, EyeOff } from "lucide-react";
import "../styles/login.css";
import bgImage from "../assets/login-bg.jpeg";

export default function Login() {

  const navigate = useNavigate();
  const { login, isAuthenticated } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  /* Redirect if already logged in */

  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  const handleLogin = (e) => {

    e.preventDefault();

    if (!email.trim() || !password.trim()) {
      setError("Email and Password are required");
      return;
    }

    setLoading(true);
    setError("");

    setTimeout(() => {

      if (email === "admin@lexihire.com" && password === "admin123") {

        const fakeUser = {
          name: "Admin User",
          email,
          role: "admin",
        };

        const fakeToken = "dummy-jwt-token";

        login(fakeUser, fakeToken, remember);

        navigate("/dashboard");

      } else {

        setError("Invalid email or password");

      }

      setLoading(false);

    }, 1000);
  };

  return (

    <div className="login-page" style={{ backgroundImage: `url(${bgImage})` }}>

      <div className="glass-container">

        <div className="brand">
          <div className="brand-dot"></div>
          <span>LexiHire</span>
        </div>

        <div className="content">

          <div className="login-card">

            <h2>Login</h2>

            <form onSubmit={handleLogin}>

              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <div className="password-wrapper">

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />

                <button
                  type="button"
                  className="eye-btn"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff size={18}/> : <Eye size={18}/>}
                </button>

              </div>

              <div className="remember-row">

                <label className="remember-left">

                  <input
                    type="checkbox"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                  />

                  <span>Remember me</span>

                </label>

                <Link to="/reset-password" className="forgot-link">
                  Forgot Password?
                </Link>

              </div>

              {error && <p className="error-text">{error}</p>}

              <button
                type="submit"
                className="login-btn"
                disabled={loading}
              >
                {loading ? "Logging in..." : "Login"}
              </button>

            </form>

          </div>

        </div>

      </div>

    </div>

  );

}