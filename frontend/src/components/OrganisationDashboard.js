import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const OrganisationDashboard = () => {
  const [organization, setOrganization] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch organization data from localStorage or API
    const orgEmail = localStorage.getItem("contact_email");

    if (!orgEmail) {
      navigate("/login-organisation");  // Redirect to login if no email found
    } else {
      // Fetch organization details from API (if required)
      // For this example, we will mock it as an object
      setOrganization({
        name: "Sample Organisation",
        email: orgEmail,
        town: "Sample Town",
        industry: "Healthcare",
        contact_number: "123-456-789",
      });
    }
  }, [navigate]);

  const handleLogout = () => {
    // Clear the localStorage or any stored session data
    localStorage.removeItem("contact_email");
    navigate("/login-organisation");  // Redirect to login page after logout
  };

  return (
    <div style={styles.container}>
      <h2>Organisation Dashboard</h2>
      {organization ? (
        <div>
          <h3>Welcome, {organization.name}</h3>
          <p><strong>Email:</strong> {organization.email}</p>
          <p><strong>Industry:</strong> {organization.industry}</p>
          <p><strong>Town:</strong> {organization.town}</p>
          <p><strong>Contact Number:</strong> {organization.contact_number}</p>
          
          {/* Add more organization-specific content here */}
          <button onClick={handleLogout} style={styles.button}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

const styles = {
  container: {
    width: "400px",
    margin: "40px auto",
    padding: "30px",
    textAlign: "center",
    border: "1px solid #ccc",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  },
  button: {
    padding: "10px",
    fontSize: "16px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default OrganisationDashboard;
