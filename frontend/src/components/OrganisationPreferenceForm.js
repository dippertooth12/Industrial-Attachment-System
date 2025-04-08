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
    preferred_field: "",
    required_skill: "",
  });

  const [fields, setFields] = useState([]);
  const [skills, setSkills] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const idToUse = orgId || localStorage.getItem("organisation_id");

    if (!idToUse) {
      setErrorMessage("No organisation ID found. Redirecting to login...");
      setTimeout(() => navigate("/login-organisation"), 2000);
      return;
    }

    if (orgId && localStorage.getItem("organisation_id") !== orgId) {
      localStorage.setItem("organisation_id", orgId);
    }

    // Fetch fields and skills from the backend
    axios.get("http://localhost:8000/api/preferred-fields/")
      .then((res) => setFields(res.data))
      .catch(() => setFields([]));

    axios.get("http://localhost:8000/api/skills/")
      .then((res) => setSkills(res.data))
      .catch(() => setSkills([]));

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
      setErrorMessage("Invalid organisation session. Please login again.");
      return;
    }

    try {
      await axios.post(
        `http://localhost:8000/api/organisation/${organisationId}/preferences/create/`,
        {
          ...formData,
          organisation: parseInt(organisationId),
          preferred_fields: [formData.preferred_field],
          required_skills: [formData.required_skill],
        },
        { headers: { "Content-Type": "application/json" } }
      );
      navigate("/organisation-dashboard");
    } catch (error) {
      setErrorMessage(error.response?.data?.error || "Submission failed");
    }
  };

  if (loading) return <div style={styles.loading}>Loading...</div>;

  return (
    <div style={styles.container}>
      <h2>Create Organisation Preference</h2>
      {errorMessage && <p style={styles.error}>{errorMessage}</p>}
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          name="pref_education_level"
          placeholder="Preferred Education Level"
          value={formData.pref_education_level}
          onChange={handleChange}
          required
          style={styles.input}
        />
        

        
        <input
          name="positions_available"
          type="number"
          placeholder="Positions Available"
          value={formData.positions_available}
          onChange={handleChange}
          required
          style={styles.input}
        />
        <div> 
        <label>Start Date</label>
        <input
          name="start_date"
          type="date"
          value={formData.start_date}
          onChange={handleChange}
          required
          style={styles.input}
        />
        </div>
        
         <div>
         <label>End Date</label>
        <input
          name="end_date"
          type="date"
          value={formData.end_date}
          onChange={handleChange}
          required
          style={styles.input}
        />
        </div>

        {/* Dropdown for Preferred Fields */}
        <select
          name="preferred_field"
          value={formData.preferred_field}
          onChange={handleChange}
          required
          style={styles.input}
        >
          <option value="">Select Preferred Field</option>
          {fields.map(field => (
            <option key={field.field_id} value={field.field_id}>
              {field.field_name}
            </option>
          ))}
        </select>

        {/* Dropdown for Required Skills */}
        <select
          name="required_skill"
          value={formData.required_skill}
          onChange={handleChange}
          required
          style={styles.input}
        >
          <option value="">Select Required Skill</option>
          {skills.map(skill => (
            <option key={skill.skill_id} value={skill.skill_id}>
              {skill.name}
            </option>
          ))}
        </select>

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