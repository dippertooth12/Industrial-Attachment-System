import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Student components
import StudentRegister from "./components/StudentRegister";
import StudentLogin from "./components/studentlogin";

// Organisation components
import OrganisationRegister from "./components/OrganisationRegister";
import OrganisationLogin from "./components/OrganisationLogin";

// Shared components
import Dashboard from "./components/Dashboard";
import Homepage from "./components/Homepage";

function App() {
  return (
    <Router>
      <Routes>
        {/* Home */}
        <Route path="/" element={<Homepage />} />

        {/* Student */}
        <Route path="/login" element={<StudentLogin />} />
        <Route path="/register" element={<StudentRegister />} />

        {/* Organisation */}
        <Route path="/login_organisation" element={<OrganisationLogin />} />
        <Route path="/register-organisation" element={<OrganisationRegister />} />

        {/* Common */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;



