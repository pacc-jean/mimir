import { Link, useNavigate } from "react-router-dom";

const Navbar = ({ sidebarOpen, setSidebarOpen }) => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={{ ...styles.sidebar, width: sidebarOpen ? "200px" : "50px" }}>
      <button onClick={() => setSidebarOpen(!sidebarOpen)} style={styles.toggleButton}>
        {sidebarOpen ? "←" : "→"}
      </button>
      {sidebarOpen && <h2 style={styles.logo}>Mimir</h2>}
      <div style={styles.links}>
        <Link to="/" style={styles.link}>🏠 {sidebarOpen ? "Home" : ""}</Link>
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
    padding: "20px",
    transition: "width 0.3s ease-in-out",
  },
  toggleButton: {
    background: "none",
    border: "none",
    color: "#fff",
    fontSize: "20px",
    cursor: "pointer",
    marginBottom: "20px",
  },
  logo: {
    marginBottom: "30px",
    fontSize: "24px",
  },
  links: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
    width: "100%",
    alignItems: "flex-start",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
    fontSize: "18px",
    padding: "10px 15px",
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  button: {
    background: "none",
    border: "none",
    cursor: "pointer",
  },
};

export default Navbar;
