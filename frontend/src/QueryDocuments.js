import React, { useState } from 'react';
import axios from 'axios';

function QueryDocuments() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [docLink, setDocLink] = useState('');
  const [error, setError] = useState('');

  const containerStyle = {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    backgroundColor: '#fff',
  };

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
          headers: {
            'Content-Type': 'application/json',
          }
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
    <div style={containerStyle}>
      <h2>Query Documents</h2>
      <form onSubmit={handleQuery}>
        <div style={{ marginBottom: 10 }}>
          <label>Question:</label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ display: 'block', width: '100%', marginTop: 5 }}
            placeholder="Enter your question"
            required
          />
        </div>
        <button type="submit">Search</button>
      </form>

      {answer && (
        <div style={{ marginTop: 10 }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
      {docLink && (
        <div style={{ marginTop: 10 }}>
          <h4>Reference Link:</h4>
          <a href={docLink} target="_blank" rel="noopener noreferrer">
            View Document Paragraph
          </a>
        </div>
      )}
      {error && <p style={{ color: 'red', marginTop: 10 }}>{error}</p>}
    </div>
  );
}

export default QueryDocuments;
