import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

export default function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  /* ===== PASSWORD STRENGTH LOGIC ===== */
  const getPasswordStrength = (password) => {
    if (!password) return { label: "", color: "" };

    let score = 0;

    if (password.length >= 6) score++;
    if (password.match(/[A-Z]/)) score++;
    if (password.match(/[0-9]/)) score++;
    if (password.match(/[^A-Za-z0-9]/)) score++;

    if (score <= 1)
      return { label: "Weak", color: "#e74c3c" };
    if (score === 2 || score === 3)
      return { label: "Medium", color: "#f39c12" };
    if (score >= 4)
      return { label: "Strong", color: "#2ecc71" };
  };

  const strength = getPasswordStrength(newPassword);

  const handleReset = (e) => {
    e.preventDefault();
    setMessage("");

    if (!newPassword || !confirmPassword) {
      setMessage("All fields are required");
      return;
    }

    if (newPassword.length < 6) {
      setMessage("Password must be at least 6 characters");
      return;
    }

    if (newPassword !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    localStorage.setItem("adminPassword", newPassword);
    setMessage("Password updated successfully!");

    setTimeout(() => {
      navigate("/login");
    }, 1500);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        {/* LEFT PANEL */}
        <div className="login-left">
          <div className="login-brand">LexiHire</div>
          <h1>Reset Password</h1>
          <p>
            Update your password to securely access your HR dashboard.
          </p>
        </div>

        {/* RIGHT PANEL */}
        <div className="login-right">
          <h2>Change Password</h2>
          <p className="login-subtitle">
            Enter and confirm your new password
          </p>

          <form onSubmit={handleReset} noValidate>

            {/* New Password */}
            <div className="input-group password-group">
              <input
                type={showNewPassword ? "text" : "password"}
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />

              <button
                type="button"
                className="toggle-password"
                onClick={() =>
                  setShowNewPassword(!showNewPassword)
                }
              >
                {showNewPassword ? "Hide" : "Show"}
              </button>
            </div>

            {/* Strength Indicator */}
            {newPassword && (
              <div
                style={{
                  marginBottom: "12px",
                  fontSize: "14px",
                  fontWeight: "600",
                  color: strength.color,
                }}
              >
                Password Strength: {strength.label}
              </div>
            )}

            {/* Confirm Password */}
            <div className="input-group password-group">
              <input
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) =>
                  setConfirmPassword(e.target.value)
                }
              />

              <button
                type="button"
                className="toggle-password"
                onClick={() =>
                  setShowConfirmPassword(!showConfirmPassword)
                }
              >
                {showConfirmPassword ? "Hide" : "Show"}
              </button>
            </div>

            {message && (
              <div className="login-error">{message}</div>
            )}

            <button type="submit" className="login-btn">
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
