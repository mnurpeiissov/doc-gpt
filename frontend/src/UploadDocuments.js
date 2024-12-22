import React, { useState } from 'react';
import axios from 'axios';

function UploadDocuments() {
  const [files, setFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

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

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/documents`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percent = Math.round(
                (progressEvent.loaded * 100) / progressEvent.total
              );
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
    <div className="container">
      <h2>Upload Documents</h2>
      <form onSubmit={handleUpload}>
        <label className="label">Choose files (txt/docx/pdf):</label>
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          accept=".txt,.docx,.pdf"
          className="input-file"
        />
        <button type="submit" className="button">Upload</button>
      </form>

      {uploadProgress > 0 && (
        <div className="progress-bar-container">
          <div
            className="progress-bar"
            style={{ width: `${uploadProgress}%` }}
          />
        </div>
      )}

      {message && <p className="message">{message}</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default UploadDocuments;
