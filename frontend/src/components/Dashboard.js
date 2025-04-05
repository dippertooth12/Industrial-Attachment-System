import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
    const navigate = useNavigate();

    const handleLogout = () => {
        // Clear any authentication data if needed
        console.log("User logged out");
        navigate('/login'); // Redirect back to login page
    };
    
    const goToPreferenceForm = () => {
        navigate("/submit-preference");
      };

    return (
        <div className="dashboard-container">
            <h2>Welcome to the Student Dashboard</h2>
            <p>You have successfully logged in.</p>
            <button onClick={handleLogout} className="logout-button">Logout</button>
            <button onClick={goToPreferenceForm} style={styles.button}>
            Submit Preferences
            </button>
        </div>
    );
};
const styles = {
    container: {
      padding: "40px",
      textAlign: "center",
    },
    button: {
      marginTop: "20px",
      padding: "10px 20px",
      fontSize: "16px",
      backgroundColor: "#007bff",
      color: "#fff",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
    },
  };
  

export default Dashboard;
