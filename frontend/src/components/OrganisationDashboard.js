import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const OrganisationDashboard = () => {
  const [organization, setOrganization] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const orgEmail = localStorage.getItem("contact_email");
    const orgName = localStorage.getItem("org_name"); // You can store this during login if needed

    if (!orgEmail) {
      navigate("/login-organisation");
    } else {
      setOrganization({
        name: orgName || "Your Organisation",
        email: orgEmail,
      });
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("contact_email");
    localStorage.removeItem("organisation_id");
    localStorage.removeItem("org_name");
    navigate("/login-organisation");
  };

  const handleSubmitPreference = () => {
    const orgId = localStorage.getItem("organisation_id");
    navigate(`/organisation/${orgId}/preferences/create`);
  };

  return (
    <div style={styles.container}>
      <h2>Organisation Dashboard</h2>
      {organization ? (
        <div>
          <h3>Welcome, {organization.name}</h3>

          <div style={styles.buttonRow}>
  <button onClick={handleLogout} style={{ ...styles.button, backgroundColor: "#dc3545" }}>
    Logout
  </button>

  <button onClick={handleSubmitPreference} style={styles.button}>
    Submit Preference
  </button>
</div>
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
    padding: "10px 20px",
    fontSize: "16px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default OrganisationDashboard;