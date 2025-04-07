import React, { useState } from "react";
import axios from "axios";

const OrganisationRegister = () => {
  const [formData, setFormData] = useState({
    org_name: '',
    industry_name: '',
    town: '',
    street: '',
    plot_number: '',
    contact_number: '',
    contact_email: '',
    password: '',
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const industries = ["Software", "Healthcare", "Finance", "Education"];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register-organisation/", formData);
      
      // Store organisation_id
      localStorage.setItem("organisation_id", response.data.organisation.id);
      localStorage.setItem("contact_email", response.data.organisation.contact_email);

      setMessage("Organisation registered successfully!");
      setFormData({
        org_name: '',
        industry_name: '',
        town: '',
        street: '',
        plot_number: '',
        contact_number: '',
        contact_email: '',
        password: '',
      });
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Organisation Registration</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input name="org_name" placeholder="Organisation Name" value={formData.org_name} onChange={handleChange} required style={styles.input} />
        <select name="industry_name" value={formData.industry_name} onChange={handleChange} required style={styles.input}>
          <option value="">Select Industry</option>
          {industries.map((industry, index) => (
            <option key={index} value={industry}>{industry}</option>
          ))}
        </select>
        <input name="town" placeholder="Town" value={formData.town} onChange={handleChange} required style={styles.input} />
        <input name="street" placeholder="Street" value={formData.street} onChange={handleChange} required style={styles.input} />
        <input name="plot_number" placeholder="Plot Number" value={formData.plot_number} onChange={handleChange} required style={styles.input} />
        <input name="contact_number" placeholder="Contact Number" value={formData.contact_number} onChange={handleChange} required style={styles.input} />
        <input name="contact_email" type="email" placeholder="Contact Email" value={formData.contact_email} onChange={handleChange} required style={styles.input} />
        <input name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange} required style={styles.input} />
        <button type="submit" style={styles.button}>Register</button>
        {message && <p style={{ ...styles.message, color: 'green' }}>{message}</p>}
        {error && <p style={{ ...styles.message, color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

const styles = {
  container: {
    width: '400px',
    margin: '40px auto',
    padding: '30px',
    textAlign: 'center',
    border: '1px solid #ccc',
    borderRadius: '10px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px',
    fontSize: '16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  message: {
    marginTop: '15px',
  },
};

export default OrganisationRegister;
