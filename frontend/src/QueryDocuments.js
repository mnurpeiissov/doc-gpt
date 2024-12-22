import React, { useState } from 'react';
import axios from 'axios';

function QueryDocuments() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [docLink, setDocLink] = useState('');
  const [error, setError] = useState('');

  const handleQuery = async (e) => {
    e.preventDefault();
    setAnswer('');
    setDocLink('');
    setError('');

    if (!query.trim()) {
      setError('Query is empty.');
      return;
    }

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/query`,
        { query },
        {
          headers: { 'Content-Type': 'application/json' }
        }
      );

      if (response.data.answer) {
        setAnswer(response.data.answer);
      }
      if (response.data.document_link) {
        setDocLink(response.data.document_link);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Query failed.');
    }
  };

  return (
    <div className="container">
      <h2>Query Documents</h2>
      <form onSubmit={handleQuery}>
        <label className="label">Question:</label>
        <input
          type="text"
          className="input-text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your question"
          required
        />
        <button type="submit" className="button">Search</button>
      </form>

      {answer && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
      {docLink && (
        <div style={{ marginTop: '1rem' }}>
          <h4>Reference Link:</h4>
          <a href={docLink} target="_blank" rel="noopener noreferrer">
            View Document Paragraph
          </a>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default QueryDocuments;
