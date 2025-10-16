import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import ReportIncident from './pages/ReportIncident';
import Dashboard from './pages/Dashboard';
import EmergencyContacts from './pages/EmergencyContacts';
import EmergencyHelp from './pages/EmergencyHelp';

const App = () => {
  const navStyle = {
    backgroundColor: '#1a365d',
    padding: '1rem',
    marginBottom: '2rem',
  };

  const navListStyle = {
    display: 'flex',
    justifyContent: 'center',
    gap: '2rem',
    listStyle: 'none',
    margin: 0,
    padding: 0,
  };

  const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '1.1rem',
  };

  return (
    <Router>
      <div>
        <nav style={navStyle}>
          <ul style={navListStyle}>
            <li>
              <Link to="/" style={linkStyle}>Home</Link>
            </li>
            <li>
              <Link to="/report" style={linkStyle}>Report Incident</Link>
            </li>
            <li>
              <Link to="/dashboard" style={linkStyle}>Dashboard</Link>
            </li>
            <li>
              <Link to="/emergency-contacts" style={linkStyle}>Emergency Contacts</Link>
            </li>
            <li>
              <Link to="/help" style={{
                ...linkStyle,
                backgroundColor: '#e53e3e',
                padding: '8px 16px',
                borderRadius: '4px',
                fontWeight: 'bold'
              }}>EMERGENCY HELP</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/report" element={<ReportIncident />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/emergency-contacts" element={<EmergencyContacts />} />
          <Route path="/help" element={<EmergencyHelp />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;