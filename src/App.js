// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import FaceRecognitionPage from './components/FaceRecognitionPage'; 
import DashboardPage from './components/DashboardPage';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/face-recognition" element={<FaceRecognitionPage />} /> {/* Updated route */}
                <Route path="/" element={<FaceRecognitionPage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
            </Routes>
        </Router>
    );
}

export default App;
