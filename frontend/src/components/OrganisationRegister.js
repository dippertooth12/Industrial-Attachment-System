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

  // Static list of industries
  const industries = ["Software", "Healthcare", "Finance", "Education"];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register-organisation/", formData);
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
    } catch (error) {
      setMessage(error.response?.data?.error || "Registration failed.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Organisation Registration</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input name="org_name" placeholder="Organisation Name" onChange={handleChange} value={formData.org_name} required style={styles.input} />
        
        {/* Industry Dropdown */}
        <select name="industry_name" onChange={handleChange} value={formData.industry_name} required style={styles.input}>
          <option value="">Select Industry</option>
          {industries.map((industry, index) => (
            <option key={index} value={industry}>{industry}</option>
          ))}
        </select>

        <input name="town" placeholder="Town" onChange={handleChange} value={formData.town} required style={styles.input} />
        <input name="street" placeholder="Street" onChange={handleChange} value={formData.street} required style={styles.input} />
        <input name="plot_number" placeholder="Plot Number" onChange={handleChange} value={formData.plot_number} required style={styles.input} />
        <input name="contact_number" placeholder="Contact Number" onChange={handleChange} value={formData.contact_number} required style={styles.input} />
        <input name="contact_email" placeholder="Contact Email" type="email" onChange={handleChange} value={formData.contact_email} required style={styles.input} />
        <input name="password" placeholder="Password" type="password" onChange={handleChange} value={formData.password} required style={styles.input} />
        <button type="submit" style={styles.button}>Register</button>
      </form>
      {message && <p style={styles.message}>{message}</p>}
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
    color: '#333',
  },
};

export default OrganisationRegister;
