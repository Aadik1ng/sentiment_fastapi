import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './App';

function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = new URLSearchParams();
    userData.append('username', email);
    userData.append('password', password);

    try {
      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: userData,
      });

      if (response.ok) {
        const data = await response.json();
        login(data.access_token);
        navigate('/upload');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed');
      }
    } catch (err) {
      setError('Error during login: ' + err.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <div>{error}</div>}
      <form onSubmit={handleSubmit}>
        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
