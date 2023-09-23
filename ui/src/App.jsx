// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Books from './pages/Books';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div>
        <Navbar />

        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Books />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
