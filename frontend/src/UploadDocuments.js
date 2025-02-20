import React, { useState } from 'react';
import axios from 'axios';

function UploadDocuments() {
  const [files, setFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Some inline styling to keep things minimal
  const containerStyle = {
    maxWidth: '600px',
    margin: '20px auto',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    backgroundColor: '#fff',
  };

  const progressBarContainerStyle = {
    height: '8px',
    backgroundColor: '#eee',
    borderRadius: '4px',
    marginTop: '10px',
    overflow: 'hidden',
  };

  const progressBarStyle = {
    height: '100%',
    width: `${uploadProgress}%`,
    backgroundColor: '#007bff',
    transition: 'width 0.3s ease',
  };

  const handleFileChange = (e) => {
    setFiles(e.target.files);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    setUploadProgress(0);

    if (!files.length) {
      setError('No files selected.');
      return;
    }

    try {
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }

      // Adjust URL to point to your FastAPI endpoint
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/documents`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              setUploadProgress(percent);
            }
          },
        }
      );

      setMessage(response.data.status);
      setUploadProgress(100);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Upload failed.');
    }
  };

  return (
    <div style={containerStyle}>
      <h2>Upload Documents</h2>
      <form onSubmit={handleUpload}>
        <div style={{ marginBottom: 10 }}>
          <label>Choose files (txt/docx/pdf):</label>
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            accept=".txt,.docx,.pdf,image/png, image/jpeg, image/jpg, image/gif, image/webp"
            style={{ display: 'block', marginTop: 5 }}
          />
        </div>
        <button type="submit">Upload</button>
      </form>

      {uploadProgress > 0 && (
        <div style={progressBarContainerStyle}>
          <div style={progressBarStyle} />
        </div>
      )}

      {message && <p style={{ color: 'green', marginTop: 10 }}>{message}</p>}
      {error && <p style={{ color: 'red', marginTop: 10 }}>{error}</p>}
    </div>
  );
}

export default UploadDocuments;
