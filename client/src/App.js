import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Navbar from "./components/Navbar";
import CategoryPage from "./components/CategoryPage";
import ProtectedRoute from "./components/ProtectedRoute";
import { useState } from "react";

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true); // Sidebar state

  return (
    <div style={styles.appContainer}>
      <Navbar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
      <div
        style={{
          ...styles.mainContent,
          marginLeft: sidebarOpen ? "220px" : "70px", // More space to prevent overlap
        }}
      >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            {<Route path="/categories/:categoryId" element={<CategoryPage />} />}
          </Route>
        </Routes>
      </div>
    </div>
  );
}

const styles = {
  appContainer: {
    display: "flex",
  },
  mainContent: {
    flex: 1,
    padding: "20px",
    transition: "margin-left 0.3s ease-in-out",
    minHeight: "100vh",
  },
};

export default App;
