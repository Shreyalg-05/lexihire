import { useState } from "react";
import "../styles/login.css";

export default function ResetPassword() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

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
  };

  return (
    <div className="reset-page">
      <div className="reset-card">
        <h1>Reset Password</h1>
        <p>Update your password to securely access your HR dashboard.</p>

        <form onSubmit={handleSubmit}>

          <div className="password-group">
            <input
              type={showNew ? "text" : "password"}
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <button type="button" onClick={() => setShowNew(!showNew)}>
              {showNew ? "Hide" : "Show"}
            </button>
          </div>

          <div className="password-group">
            <input
              type={showConfirm ? "text" : "password"}
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
            <button type="button" onClick={() => setShowConfirm(!showConfirm)}>
              {showConfirm ? "Hide" : "Show"}
            </button>
          </div>

          {message && <div className="reset-message">{message}</div>}

          <button type="submit" className="reset-btn">
            Update Password
          </button>

        </form>
      </div>
    </div>
  );
}
