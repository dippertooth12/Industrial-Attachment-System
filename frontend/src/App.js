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

// Shared Components
import Dashboard from "./components/Dashboard";
import Homepage from "./components/Homepage";

// Wrapper for dynamic orgId route
const OrganisationPreferenceFormWrapper = () => {
  const { orgId } = useParams();
  return <OrganisationPreferenceForm orgId={orgId} />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Homepage */}
        <Route path="/" element={<Homepage />} />

        {/* Student Routes */}
        <Route path="/login" element={<StudentLogin />} />
        <Route path="/register" element={<StudentRegister />} />

        {/* Organisation Routes */}
        <Route path="/login-organisation" element={<OrganisationLogin />} />
        <Route path="/register-organisation" element={<OrganisationRegister />} />
        <Route path="/organisation-dashboard" element={<OrganisationDashboard />} />
        <Route path="/organisation/:orgId/preferences/create" element={<OrganisationPreferenceFormWrapper />} />

        {/* Shared Dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
