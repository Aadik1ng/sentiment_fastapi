import React, { useState, createContext, useContext } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Signup from './Signup';
import Login from './Login';
import SentimentUpload from './SentimentUpload';

const AuthContext = createContext();

function App() {
  const [auth, setAuth] = useState({ token: null });

  const login = (token) => {
    setAuth({ token });
  };

  const logout = () => {
    setAuth({ token: null });
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      <Router>
        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route
            path="/upload"
            element={auth.token ? <SentimentUpload token={auth.token} /> : <Navigate to="/login" />}
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthContext.Provider>
  );
}

export default App;
export const useAuth = () => useContext(AuthContext);
