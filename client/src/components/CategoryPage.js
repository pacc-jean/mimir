import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const CategoryPage = () => {
  const { categoryId } = useParams();
  const [category, setCategory] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5000/categories/${categoryId}`)
      .then((res) => res.json())
      .then((data) => setCategory(data))
      .catch((err) => console.error("Error fetching category:", err));
  }, [categoryId]);

  if (!category) {
    return <p>Loading category...</p>;
  }

  return (
    <div style={styles.container}>
      <h2>{category.name}</h2>
      <div style={styles.communityList}>
        {category.communities.length > 0 ? (
          category.communities.map((community) => (
            <div key={community.id} style={styles.communityBox}>
              <h3>{community.name}</h3>
              <p>{community.description}</p>
              <p style={{ color: "#333", fontWeight: "bold" }}>
                <strong>Members:</strong> {community.members_count}
              </p>
            </div>
          ))
        ) : (
          <p>No communities in this category yet.</p>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: { padding: "20px" },
  communityList: { display: "flex", flexDirection: "column", gap: "10px" },
  communityBox: {
    padding: "10px",
    border: "1px solid #ddd",
    borderRadius: "5px",
    backgroundColor: "#f9f9f9",
  },
};

export default CategoryPage;
