import { Link, useLocation } from "react-router-dom";
import { useEffect } from "react";
import "../styles/home.css";

export default function Navbar({ onLoginClick }) {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  useEffect(() => {
    const pill = document.querySelector(".navbar-pill");
    if (!pill) return;

    const onScroll = () => {
      if (window.scrollY > 20) {
        pill.classList.add("scrolled");
      } else {
        pill.classList.remove("scrolled");
      }
    };

    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className="navbar-wrapper">
      <div className="navbar-pill">
        <div className="logo">
          <Link to="/">LexiHire</Link>
        </div>

        <nav>
          <Link to="/" className={isActive("/") ? "active-link" : ""}>
            Home
          </Link>
          <Link
            to="/how-it-works"
            className={isActive("/how-it-works") ? "active-link" : ""}
          >
            How it works
          </Link>
          <Link
            to="/about"
            className={isActive("/about") ? "active-link" : ""}
          >
            About
          </Link>

          <Link to="/login" className="btn-outline">
            Login
          </Link>
        </nav>
      </div>
    </header>
  );
}
