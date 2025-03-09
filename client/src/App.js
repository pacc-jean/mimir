import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";


function App() {
  return (
    <div>
      <h1>Welcome to Mimir</h1>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        {/* Protected Routes */}
        <Route element={<ProtectedRoute />}>
          {/* Add protected routes here */}
          {/* Example: <Route path="/dashboard" element={<Dashboard />} /> */}
        </Route>
      </Routes>
    </div>
  );
}

export default App;
