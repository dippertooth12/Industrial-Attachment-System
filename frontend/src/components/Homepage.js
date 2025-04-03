import React from 'react';
import {useNavigate} from 'react-router-dom';

const Homepage = () => {
    const navigate = useNavigate(); //useNavigate for routing

    //navigate to student login page when button is clicked
    const handleStudentLoginClick = () => {
        navigate('/login');
    };

    // Inline styles
  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#f4f4f9',
    },
    header: {
      fontSize: '2.5rem',
      marginBottom: '40px',
    },
    buttons: {
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
    },
    button: {
      width: '200px',
      height: '50px',
      border: 'none',
      borderRadius: '30px',
      fontSize: '1.2rem',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
    },
    buttonHover: {
      backgroundColor: '#82c4e5', // Soft blue hover effect
    },
    buttonPink: {
      backgroundColor: '#f7c1b2', // Soft pink
    },
    buttonGreen: {
      backgroundColor: '#bfe3c0', // Soft green
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Industrial Attachment System</h1>
      <div style={styles.buttons}>
        <button
          style={{ ...styles.button, ...styles.buttonGreen }}
          onClick={handleStudentLoginClick}
        >
          Student Login
        </button>
        <button style={{ ...styles.button, ...styles.buttonPink }}>
          Organization Login
        </button>
        <button style={{ ...styles.button, ...styles.buttonPink }}>
          Supervisor Login
        </button>
      </div>
    </div>
  );
};

export default Homepage;