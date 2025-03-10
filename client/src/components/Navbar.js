import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { FaInstagram, FaTwitter, FaReddit, FaGithub, FaLinkedin, FaWhatsapp, FaEnvelope, FaYoutube, FaThList } from "react-icons/fa";
import CategoriesModal from "./CategoriesModal";


const Navbar = ({ sidebarOpen, setSidebarOpen }) => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // State for categories modal
  const [showCategories, setShowCategories] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={{ ...styles.sidebar, width: sidebarOpen ? "200px" : "50px" }}>
      <button onClick={() => setSidebarOpen(!sidebarOpen)} style={styles.toggleButton}>
        {sidebarOpen ? "←" : "→"}
      </button>

      {/* Mimir Title */}
      {sidebarOpen && <h2 style={styles.logo}>Mimir</h2>}
      <hr style={styles.divider} />

      {/* Navigation Links */}
      <div style={styles.links}>
        <Link to="/" style={styles.link}>🏠 {sidebarOpen ? "Home" : ""}</Link>
        <button onClick={() => setShowCategories(true)} style={{ ...styles.link, ...styles.button }}>
          <FaThList /> {sidebarOpen ? "Categories" : ""}
        </button>
        {!token ? (
          <>
            <Link to="/login" style={styles.link}>🔑 {sidebarOpen ? "Login" : ""}</Link>
            <Link to="/register" style={styles.link}>📝 {sidebarOpen ? "Register" : ""}</Link>
          </>
        ) : (
          <button onClick={handleLogout} style={{ ...styles.link, ...styles.button }}>
            🚪 {sidebarOpen ? "Logout" : ""} 
          </button>
        )}
      </div>
      <hr style={styles.divider} />

      {/* Contact Us Section */}
      <div style={styles.contactSection}>
        {sidebarOpen && <h3 style={styles.contactTitle}>Contact Us</h3>}
        <div style={styles.socialIcons}>
          <a href="https://www.instagram.com/ean.lc/" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaInstagram />
          </a>
          <a href="https://x.com/plaidpeanuts" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaTwitter />
          </a>
          <a href="https://www.reddit.com/user/Signal_Function6946/" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaReddit />
          </a>
          <a href="https://github.com/pacc-jean" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaGithub />
          </a>
          <a href="https://www.linkedin.com/in/jean-kajuga-080018315/" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaLinkedin />
          </a>
          <a href="https://wa.me/+25469845876" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaWhatsapp />
          </a>
          <a href="mailto:jeanluc.xii.iv@gmail.com" style={styles.icon}>
            <FaEnvelope />
          </a>
          <a href="https://www.youtube.com/@plaidpeanuts" target="_blank" rel="noopener noreferrer" style={styles.icon}>
            <FaYoutube />
          </a>
        </div>
      </div>

      {/* Categories Modal */}
      {showCategories && <CategoriesModal onClose={() => setShowCategories(false)} />}
    </nav>
  );
};

const styles = {
  sidebar: {
    position: "fixed",
    top: 0,
    left: 0,
    height: "100vh",
    backgroundColor: "#333",
    color: "#fff",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "10px",
    transition: "width 0.3s ease-in-out",
    justifyContent: "space-between",
  },
  toggleButton: {
    background: "none",
    border: "none",
    color: "#fff",
    fontSize: "20px",
    cursor: "pointer",
    marginBottom: "10px",
  },
  logo: {
    fontSize: "22px",
    marginBottom: "10px",
  },
  divider: {
    width: "100%",
    height: "1px",
    backgroundColor: "#555",
    margin: "5px 0",
  },
  links: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    width: "100%",
    alignItems: "flex-start",
    flexGrow: 1,
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "16px",
    padding: "8px 12px",
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  button: {
    background: "none",
    border: "none",
    cursor: "pointer",
  },
  contactSection: {
    textAlign: "center",
    paddingBottom: "10px",
  },
  contactTitle: {
    fontSize: "14px",
    marginBottom: "5px",
  },
  socialIcons: {
    display: "flex",
    gap: "8px",
    flexWrap: "wrap",
    justifyContent: "center",
  },
  icon: {
    color: "#fff",
    fontSize: "18px",
    textDecoration: "none",
  },
};

export default Navbar;
