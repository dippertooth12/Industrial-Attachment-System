import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

const StudentLogin = () => {
  const [formData, setFormData] = useState({
    student_id: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", formData, {
        headers:{
          "Content-Type": "application/json",
        },
      });
      setMessage(response.data.message);

      if (response.status === 200) { // ✅ Check HTTP status instead of `response.data.success`
        localStorage.setItem("student_id", response.data.student_id); // Store login state
        navigate("/dashboard");
      }
    } catch (error) {
      setMessage(error.response?.data?.error || "Invalid Student ID or Password.");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Student Login</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input name="student_id" placeholder="Student ID" onChange={handleChange} required style={styles.input} />
        <input name="password" placeholder="Password" type="password" onChange={handleChange} required style={styles.input} />
        <button type="submit" style={styles.button}>Login</button>
      </form>
      {message && <p style={styles.message}>{message}</p>}
      <p style={styles.linkText}>
        Don't have an account? <Link to="/register" style={styles.link}>Register here</Link>
      </p>
    </div>
  );
};

const styles = {
  container: {
    width: "400px",
    margin: "40px auto",
    padding: "30px",
    textAlign: "center",
    border: "1px solid #ccc",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px",
    fontSize: "16px",
    backgroundColor: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
  message: {
    marginTop: "15px",
    color: "#333",
  },
  linkText: {
    marginTop: "15px",
    fontSize: "14px",
  },
  link: {
    color: "#007bff",
    textDecoration: "none",
  },
};

export default StudentLogin;

