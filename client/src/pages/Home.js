import React from "react";
import "./Home.css";

const Home = () => {
  return (
    <div className="home-container">
      <div className="main-content">
        {/* Left Section (Scrollable Posts Area) */}
        <div className="posts-section">
          {/* Fixed Top Section Inside Posts */}
          <div className="top-section">
            <input type="text" placeholder="Search..." className="search-bar" />
            <button className="create-community-btn">Create Community</button>
          </div>

          {/* Feed Toggle */}
          <div className="feed-toggle">
            <button className="trending-btn">Trending</button>
            <button className="your-feed-btn">Your Feed</button>
          </div>

          {/* Floating Create Post Button */}
          <button className="create-post-btn">+</button>

          {/* Scrollable Posts Container */}
          <div className="posts-container">
            <div className="post-box">Post Content</div>
            <div className="post-box">Post Content</div>
            <div className="post-box">Post Content</div>
          </div>
        </div>

        {/* Right Section (Fixed Side Panel) */}
        <div className="side-panel">
          <button className="profile-btn">Profile</button>
          <div className="live-chat">Live Chat (Auto-scroll)</div>
          <button className="admin-chat-btn">Admin Chat</button>
        </div>
      </div>
    </div>
  );
};

export default Home;
