import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const OrganisationPreferenceForm = () => {
  const { orgId } = useParams();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    pref_education_level: "",
    positions_available: "",
    start_date: "",
    end_date: "",
  });

  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const idToUse = orgId || localStorage.getItem("organisation_id");

    if (!idToUse) {
      setErrorMessage("No organisation ID found. Redirecting to login...");
      setTimeout(() => navigate("/login-organisation"), 2000);
      return;
    }

    // Sync localStorage with URL param
    if (orgId && localStorage.getItem("organisation_id") !== orgId) {
      localStorage.setItem("organisation_id", orgId);
    }

    setLoading(false);
  }, [orgId, navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const organisationId = orgId || localStorage.getItem("organisation_id");
    if (!organisationId) {
      setErrorMessage("Organisation ID is missing.");
      return;
    }

    console.log("Submitting with org ID:", organisationId);

    try {
      await axios.post(
        `http://localhost:8000/api/organisation/${organisationId}/preferences/create/`,
        formData,
        { headers: { 'Content-Type': 'application/json' } }
      );

      alert("Preference created successfully!");
      navigate("/organisation-dashboard");
    } catch (error) {
      console.error("Submission error:", error.response?.data || error.message);
      const msg =
        error.response?.data?.error ||
        JSON.stringify(error.response?.data) ||
        "Error creating preference.";
      setErrorMessage(msg);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading organisation data...</div>;
  }

  return (
    <div style={styles.container}>
      <h2>Create Organisation Preference</h2>
      {errorMessage && <p style={styles.error}>{errorMessage}</p>}

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          name="pref_education_level"
          placeholder="Preferred Education Level"
          onChange={handleChange}
          value={formData.pref_education_level}
          required
          style={styles.input}
        />
        <input
          name="positions_available"
          type="number"
          placeholder="Positions Available"
          onChange={handleChange}
          value={formData.positions_available}
          required
          style={styles.input}
          min="1"
        />
        <input
          name="start_date"
          type="date"
          onChange={handleChange}
          value={formData.start_date}
          required
          style={styles.input}
        />
        <input
          name="end_date"
          type="date"
          onChange={handleChange}
          value={formData.end_date}
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Submit</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "500px",
    margin: "40px auto",
    padding: "25px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
  },
  loading: {
    textAlign: "center",
    padding: "20px",
    fontSize: "18px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "12px",
    fontSize: "16px",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  error: {
    color: "#d32f2f",
    backgroundColor: "#fde8e8",
    padding: "10px",
    borderRadius: "5px",
    textAlign: "center",
  },
};

export default OrganisationPreferenceForm;
