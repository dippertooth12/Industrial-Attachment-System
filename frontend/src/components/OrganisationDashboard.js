import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const OrganisationDashboard = () => {
  const [organization, setOrganization] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const orgEmail = localStorage.getItem("contact_email");

    if (!orgEmail) {
      navigate("/login-organisation");
    } else {
      fetch(`http://127.0.0.1:8000/api/organisation/by-email/${orgEmail}`)
        .then(res => res.json())
        .then(data => {
          console.log(data);
          if (data.error) {
            navigate("/login-organisation");
          } else {
            setOrganization(data);

            // Also store org ID in localStorage for later use
            localStorage.setItem("organisation_id", data.id);
          }
        })
        .catch(() => navigate("/login-organisation"));
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("contact_email");
    localStorage.removeItem("organisation_id");
    navigate("/login-organisation");
  };

  const handleManagePreferences = () => {
    const orgId = localStorage.getItem("organisation_id");
    if (orgId) {
      navigate(`/organisation/${orgId}/preferences/create`);
    } else {
      navigate("/login-organisation");
    }
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

          <button onClick={handleLogout} style={styles.button}>Logout</button>

          <button
            onClick={handleManagePreferences}
            style={{ ...styles.button, backgroundColor: "#28a745", marginTop: "10px" }}
          >
            Manage Preferences
          </button>
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
