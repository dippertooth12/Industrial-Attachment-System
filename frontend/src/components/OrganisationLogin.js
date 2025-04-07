import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from "axios";

const OrganisationLogin = () => {
  const [formData, setFormData] = useState({ contact_email: '', password: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login-organisation/", formData, {
        headers: { "Content-Type": "application/json" },
      });

      setMessage("Login successful!");

      // ✅ Store both organisation_id and contact_email
      localStorage.setItem("organisation_id", response.data.organisation_id);
      localStorage.setItem("contact_email", formData.contact_email);

      navigate("/organisation-dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Invalid email or password.");
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Organisation Login</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          name="contact_email"
          value={formData.contact_email}
          onChange={handleChange}
          placeholder="Contact Email"
          required
          style={styles.input}
        />
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button}>Login</button>
        {message && <p style={{ ...styles.message, color: 'green' }}>{message}</p>}
        {error && <p style={{ ...styles.message, color: 'red' }}>{error}</p>}
      </form>
      <div style={styles.registerLinkContainer}>
        <p style={styles.registerLinkText}>
          Don't have an account? <Link to="/register-organisation" style={styles.registerLink}>Register here</Link>
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '400px',
    margin: '2rem auto',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 0 15px rgba(0,0,0,0.1)',
    backgroundColor: '#f9f9f9',
  },
  title: {
    textAlign: 'center',
    marginBottom: '1rem',
    fontSize: '1.5rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  input: {
    padding: '0.5rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '0.6rem',
    fontSize: '1rem',
    borderRadius: '6px',
    backgroundColor: '#007BFF',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
  message: {
    textAlign: 'center',
    marginTop: '1rem',
  },
  registerLinkContainer: {
    textAlign: 'center',
    marginTop: '1rem',
  },
  registerLinkText: {
    fontSize: '1rem',
  },
  registerLink: {
    color: '#007BFF',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
};

export default OrganisationLogin;
