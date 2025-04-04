import React, { useState } from 'react';
import axios from 'axios';

function PreferenceForm({ role, studentId = null, orgId = null }) {
  const [formData, setFormData] = useState({
    available_from: '',
    available_to: '',
    field: '',
    organisation_name: '',
    preferred_education_level: '',
    positions_available: ''
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const endpoint =
        role === 'student'
          ? 'http://127.0.0.1:8000/api/preferences/student/'
          : 'http://127.0.0.1:8000/api/preferences/organization/';

      const payload =
        role === 'student'
          ? {
              available_from: formData.available_from,
              available_to: formData.available_to,
              field: formData.field,
              organisation_name: formData.organisation_name,
              student_id: studentId
            }
          : {
              start_date: formData.available_from,
              end_date: formData.available_to,
              preferred_field: formData.field,
              preferred_education_level: formData.preferred_education_level,
              positions_available: formData.positions_available,
              org_id: orgId
            };

      const response = await axios.post(endpoint, payload);
      setMessage(response.data.message || 'Preferences saved successfully!');
    } catch (error) {
      setMessage(error.response?.data?.error || 'Submission failed.');
    }
  };

  return (
    <div style={styles.container}>
      <h2>{role === 'student' ? 'Student' : 'Organization'} Preferences</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <label>Available From</label>
        <input type="date" name="available_from" onChange={handleChange} style={styles.input} required />

        <label>Available To</label>
        <input type="date" name="available_to" onChange={handleChange} style={styles.input} required />

        <label>Field of Interest</label>
        <input type="text" name="field" onChange={handleChange} style={styles.input} required />

        {role === 'student' && (
          <>
            <label>Organization Name</label>
            <input type="text" name="organisation_name" onChange={handleChange} style={styles.input} required />
          </>
        )}

        {role === 'organization' && (
          <>
            <label>Positions Available</label>
            <input type="text" name="positions_available" onChange={handleChange} style={styles.input} required />

            <label>Preferred Education Level</label>
            <input type="text" name="preferred_education_level" onChange={handleChange} style={styles.input} required />
          </>
        )}

        <button type="submit" style={styles.button}>Submit Preferences</button>
      </form>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

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
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  message: {
    marginTop: '15px',
    color: '#333',
  }
};

export default PreferenceForm;