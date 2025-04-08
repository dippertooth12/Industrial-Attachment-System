import React, { useState } from 'react';

const LogbookForm = () => {
  const [formData, setFormData] = useState({
    student_id: '',
    org_id: '',
    week_number: '',
    log_entry: '',
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/api/logbook/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Logbook entry submitted successfully!');
        setFormData({ student_id: '', org_id: '', week_number: '', log_entry: '' });
      } else {
        setMessage(data.error || 'Submission failed');
      }
    } catch (error) {
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Logbook Entry</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          name="student_id"
          value={formData.student_id}
          onChange={handleChange}
          placeholder="Student ID"
          style={styles.input}
          required
        />
        <input
          type="text"
          name="org_id"
          value={formData.org_id}
          onChange={handleChange}
          placeholder="Organisation ID"
          style={styles.input}
          required
        />
        <input
          type="number"
          name="week_number"
          value={formData.week_number}
          onChange={handleChange}
          placeholder="Week Number"
          style={styles.input}
          required
        />
        <textarea
          name="log_entry"
          value={formData.log_entry}
          onChange={handleChange}
          placeholder="Log Entry"
          style={styles.textarea}
          required
        />
        <button type="submit" style={styles.button}>Submit</button>
        {message && <p style={styles.message}>{message}</p>}
      </form>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '500px',
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
  textarea: {
    padding: '0.5rem',
    fontSize: '1rem',
    borderRadius: '6px',
    border: '1px solid #ccc',
    minHeight: '100px',
  },
  button: {
    padding: '0.6rem',
    fontSize: '1rem',
    borderRadius: '6px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
  message: {
    textAlign: 'center',
    marginTop: '1rem',
    color: '#d9534f',
  },
};

export default LogbookForm;

