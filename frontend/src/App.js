// src/App.js
import React from "react";
import StudentRegister from "./components/StudentRegister";
import {BrowserRouter as Router, Routes,Route } from "react-router-dom";
import StudentLogin from "./components/studentlogin";
import Dashboard from "./components/Dashboard";
import Homepage from './components/Homepage';
import LogbookForm from './components/LogbookForm';
import OrganisationRegister from "./components/OrganisationRegister";
import OrganisationLogin from "./components/OrganisationLogin";



function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Homepage/>}/>
          <Route path="/login" element={<StudentLogin/>} />
          <Route path="/register" element={<StudentRegister/>} />
          <Route path="/login_organisation" element={<OrganisationLogin />} />
          <Route path="/register-organisation" element={<OrganisationRegister />} />
          <Route path="/dashboard" element={<Dashboard/>}/>
          <Route path="/logbook" element={<LogbookForm />} />
        </Routes>
    </Router>
  );
}

export default App;


