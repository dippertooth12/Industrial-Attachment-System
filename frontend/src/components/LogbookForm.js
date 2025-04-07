import React, { useState } from 'react';
import axios from 'axios';
import './LogbookForm.css'; // CSS in separate file

function LogbookForm() {
  const [formData, setFormData] = useState({
    student_id: '',
    org_id: '',
    week_number: '',
    log_entry: ''
  });

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/logbook', formData);
      alert('Logbook entry submitted!');
      setFormData({ student_id: '', org_id: '', week_number: '', log_entry: '' });
    } catch (err) {
      console.error(err);
      alert('Error submitting logbook');
    }
  };

  return (
    <div className="logbook-container">
      <h2 className="logbook-title">Logbook Entry</h2>
      <form className="logbook-form" onSubmit={handleSubmit}>
        <label>Student ID</label>
        <input type="text" name="student_id" value={formData.student_id} onChange={handleChange} required />

        <label>Organisation ID</label>
        <input type="text" name="org_id" value={formData.org_id} onChange={handleChange} required />

        <label>Week Number</label>
        <input type="number" name="week_number" value={formData.week_number} onChange={handleChange} required />

        <label>Log Entry</label>
        <textarea name="log_entry" value={formData.log_entry} onChange={handleChange} required />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default LogbookForm;
