// src/App.js
import React from "react";
import StudentRegister from "./components/StudentRegister";
import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import StudentLogin from "./components/studentlogin";
import Dashboard from "./components/Dashboard";
import Homepage from './components/Homepage';

function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Homepage/>}/>
          <Route path="/login" element={<StudentLogin/>} />
          <Route path="/register" element={<StudentRegister/>} />
          <Route path="/dashboard" element={<Dashboard/>}/>
          {/* You can add more routes here*/}
        </Routes>
    </Router>
  );
}

export default App;


