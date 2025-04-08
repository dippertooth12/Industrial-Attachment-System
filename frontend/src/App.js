// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route, useParams } from "react-router-dom";

// Student Components
import StudentRegister from "./components/StudentRegister";
import StudentLogin from "./components/studentlogin";

// Organisation Components
import OrganisationRegister from "./components/OrganisationRegister";
import OrganisationLogin from "./components/OrganisationLogin";
import OrganisationDashboard from "./components/OrganisationDashboard";
import OrganisationPreferenceForm from "./components/OrganisationPreferenceForm";
import PreferenceForm from "./Preferenceform"

// Shared Components
import Dashboard from "./components/Dashboard";
import Homepage from "./components/Homepage";
import LogbookForm from './components/LogbookForm';

function App() {
  console.log("Logbook route loaded");
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Homepage/>}/>
          {/* Student */}
        <Route path="/login" element={<StudentLogin />} />
        <Route path="/register" element={<StudentRegister />} />

        {/* Organisation */}
        <Route path="/login-organisation" element={<OrganisationLogin />} />
        <Route path="/register-organisation" element={<OrganisationRegister />} />

          <Route path="/dashboard" element={<Dashboard/>}/>
          <Route path="/submit-preference" element={<PreferenceForm />} />
          <Route path="/organisation-dashboard" element={<OrganisationDashboard />} />
          <Route path="/organisation/:orgId/preferences/create" element={<OrganisationPreferenceForm />}/>
          <Route path="/logbook" element={<LogbookForm />} />
          {/* You can add more routes here*/}
        </Routes>
    </Router>
  );
}

export default App;


