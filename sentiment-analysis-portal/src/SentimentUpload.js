import React, { useState } from 'react';
import { useAuth } from './App';

function SentimentUpload() {
  const { auth } = useAuth();
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze_sentiment', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${auth.token}`
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'File upload failed');
      }
    } catch (err) {
      setError('Error during file upload: ' + err.message);
    }
  };

  return (
    <div>
      <h2>Upload File for Sentiment Analysis</h2>
      {error && <div>{error}</div>}
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} required />
        <button type="submit">Upload</button>
      </form>
      {result && (
        <div>
          <h3>Sentiment Analysis Result</h3>
          <p>Positive: {result.positive_count}</p>
          <p>Neutral: {result.neutral_count}</p>
          <p>Negative: {result.negative_count}</p>
          <img src={result.bar_chart_url} alt="Bar Chart" />
          <img src={result.pie_chart_url} alt="Pie Chart" />
        </div>
      )}
    </div>
  );
}

export default SentimentUpload;
