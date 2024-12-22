import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from 'react-router-dom';

import UploadDocuments from './UploadDocuments';
import QueryDocuments from './QueryDocuments';

function Home() {
  return (
    <div>
      <h2 className="home-title">Welcome to DocGPT!!!</h2>
      <p className="home-description">
        This is DocGPT. Upload your documents and start chatting with your documents!
        <br /><br />
        Explore the “Upload” page to add your documents, and the “Query” page to ask questions or search 
        through the uploaded files. The system will respond with an answer and reference the document 
        paragraph if available.
      </p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav className="navbar">
        <Link to="/">Home</Link>
        <Link to="/upload">Upload</Link>
        <Link to="/query">Query</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadDocuments />} />
        <Route path="/query" element={<QueryDocuments />} />
      </Routes>
    </Router>
  );
}

export default App;
