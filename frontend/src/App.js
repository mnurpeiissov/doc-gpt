import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

import UploadDocuments from './UploadDocuments';
import QueryDocuments from './QueryDocuments';

function App() {
  // Minimal navigation bar styling
  const navStyle = {
    backgroundColor: '#f8f8f8',
    padding: '1rem',
    marginBottom: '1rem',
    borderBottom: '1px solid #ccc',
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  };

  const linkStyle = {
    textDecoration: 'none',
    color: '#333',
    fontWeight: 'bold',
  };

  return (
    <Router>
      <nav style={navStyle}>
        <Link to="/" style={linkStyle}>Home</Link>
        <Link to="/upload" style={linkStyle}>Upload</Link>
        <Link to="/query" style={linkStyle}>Query</Link>
      </nav>

      <Routes>
        <Route
          path="/"
          element={
            <h2 style={{ textAlign: 'center', marginTop: 20 }}>
              Welcome to FastAPI + React Document App (No Auth)!
            </h2>
          }
        />
        <Route path="/upload" element={<UploadDocuments />} />
        <Route path="/query" element={<QueryDocuments />} />
      </Routes>
    </Router>
  );
}

export default App;
