import React, { useState, useEffect } from "react";
import axios from "axios";

const StudentPreferenceForm = () => {
  const [formData, setFormData] = useState({
    student_pref_id: "",
    student_id: localStorage.getItem("student_id") || "",
    pref_location: "",
    available_from: "",
    available_to: "",
    industries: [],
    skills: [],
  });

  const [industryOptions, setIndustryOptions] = useState([]);
  const [skillOptions, setSkillOptions] = useState([]);
  const [message, setMessage] = useState("");

  // Fetch industry and skill options
  useEffect(() => {
    axios.get("http://localhost:8000/api/industries/")
      .then(res => setIndustryOptions(res.data))
      .catch(() => setIndustryOptions([]));

    axios.get("http://localhost:8000/api/skills/")
      .then(res => setSkillOptions(res.data))
      .catch(() => setSkillOptions([]));
  }, []);

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleCheckboxChange = (type, id) => {
    setFormData((prev) => {
      const selected = prev[type];
      const updated = selected.includes(id)
        ? selected.filter(item => item !== id)
        : [...selected, id];
      return { ...prev, [type]: updated };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/api/student-preference/", formData)
      setMessage("Preferences submitted successfully!");
    } catch (err) {
      setMessage(err.response?.data?.error || "Server error. Try again later.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Student Preference Form</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          name="student_pref_id"
          placeholder="Preference ID"
          value={formData.student_pref_id}
          onChange={handleChange}
          required
          style={styles.input}
        />
        <input
          name="pref_location"
          placeholder="Preferred Location"
          value={formData.pref_location}
          onChange={handleChange}
          required
          style={styles.input}
        />
        <label>Available From:</label>
        <input
          type="date"
          name="available_from"
          value={formData.available_from}
          onChange={handleChange}
          required
          style={styles.input}
        />
        <label>Available To:</label>
        <input
          type="date"
          name="available_to"
          value={formData.available_to}
          onChange={handleChange}
          required
          style={styles.input}
        />

        <h4>Select Preferred Industries:</h4>
        {industryOptions.map((industry) => (
          <label key={industry.industry_id} style={styles.checkboxLabel}>
            <input
              type="checkbox"
              onChange={() => handleCheckboxChange("industries", industry.industry_id)}
            />
            {industry.name}
          </label>
        ))}

        <h4>Select Desired Skills:</h4>
        {skillOptions.map((skill) => (
          <label key={skill.skill_id} style={styles.checkboxLabel}>
            <input
              type="checkbox"
              onChange={() => handleCheckboxChange("skills", skill.skill_id)}
            />
            {skill.name}
          </label>
        ))}

        <button type="submit" style={styles.button}>Submit</button>
      </form>

      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

const styles = {
  container: {
    width: "500px",
    margin: "30px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "10px",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "15px",
  },
  input: {
    padding: "10px",
    borderRadius: "5px",
    fontSize: "16px",
    border: "1px solid #aaa",
  },
  checkboxLabel: {
    display: "block",
    marginTop: "5px",
  },
  button: {
    padding: "10px",
    backgroundColor: "#007bff",
    color: "white",
    fontSize: "16px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  message: {
    marginTop: "10px",
    color: "#333",
  },
};

export default StudentPreferenceForm;