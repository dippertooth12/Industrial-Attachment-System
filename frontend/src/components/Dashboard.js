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

    return (
        <div className="dashboard-container">
            <h2>Welcome to the Student Dashboard</h2>
            <p>You have successfully logged in.</p>
            <button onClick={handleLogout} className="logout-button">Logout</button>
        </div>
    );
};

export default Dashboard;