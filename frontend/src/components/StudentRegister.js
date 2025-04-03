import React, { useState } from "react";
import axios from "axios";

const StudentRegister = () => {
  const [formData, setFormData] = useState({
    student_id: '',
    first_name: '',
    last_name: '',
    year_of_study: '',
    student_email: '',
    student_contact_number: '',
    password:''
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/register-student/", formData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Something went wrong.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Student Registration</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input name="student_id" placeholder="Student ID" onChange={handleChange} required style={styles.input} />
        <input name="first_name" placeholder="First Name" onChange={handleChange} required style={styles.input} />
        <input name="last_name" placeholder="Last Name" onChange={handleChange} required style={styles.input} />
        <input name="year_of_study" placeholder="Year of Study" type="number" onChange={handleChange} required style={styles.input} />
        <input name="student_email" placeholder="Email" type="email" onChange={handleChange} required style={styles.input} />
        <input name="student_contact_number" placeholder="Phone Number" onChange={handleChange} required style={styles.input} />
        <input name="password" placeholder="Password" type="password" onChange={handleChange} required style={styles.input}/>
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

export default StudentRegister;

