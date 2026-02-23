import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import "../styles/home.css";

export default function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 40);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <motion.header
      className="navbar-wrapper"
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className={`navbar-pill ${scrolled ? "navbar-scrolled" : ""}`}>

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
    </motion.header>
  );
}
