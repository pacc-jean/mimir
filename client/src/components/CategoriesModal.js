import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const CategoriesModal = ({ onClose }) => {
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  // Fetch categories from API
  useEffect(() => {
    fetch("http://localhost:5000/categories")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  // Handle category click
  const handleCategoryClick = (categoryId) => {
    navigate(`/categories/${categoryId}`);
    onClose();
  };

  return (
    <div style={styles.modalOverlay}>
      <div style={styles.modal}>
        <button onClick={onClose} style={styles.closeButton}>✖</button>
        <h3 style={{ color: "#333", fontWeight: "bold" }}>Categories</h3>
        <div style={styles.categoryList}>
          {categories.length > 0 ? (
            categories.map((category) => (
              <span 
                key={category.id} 
                style={styles.categoryBox} 
                onClick={() => handleCategoryClick(category.id)}
              >
                {category.name}
              </span>
            ))
          ) : (
            <p>Loading categories...</p>
          )}
        </div>
      </div>
    </div>
  );
};

const styles = {
  modalOverlay: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100vw",
    height: "100vh",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  modal: {
    backgroundColor: "#fff",
    padding: "20px",
    borderRadius: "10px",
    width: "300px",
    textAlign: "center",
    position: "relative",
  },
  closeButton: {
    position: "absolute",
    top: "10px",
    right: "10px",
    background: "none",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
  },
  categoryList: {
    display: "flex",
    flexWrap: "wrap",
    gap: "10px",
    marginTop: "15px",
    justifyContent: "center",
  },
  categoryBox: {
    backgroundColor: "#ddd",
    padding: "8px 12px",
    borderRadius: "8px",
    cursor: "pointer",
  },
};

export default CategoriesModal;
