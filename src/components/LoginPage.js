// src/components/LoginPage.js
import React, { useState } from 'react';
import { supabase } from '../supabaseClient';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setErrorMessage('');

        try {
            const { data, error } = await supabase
                .from('users')
                .select('*')
                .eq('university_id', username)
                .eq('password', password)
                .eq('position', 'admin');

            if (error) {
                setErrorMessage('Error: ' + error.message);
                return;
            }

            if (data && data.length > 0) {
                localStorage.setItem('university_id', username); // Save university ID
                navigate('/face-recognition'); // Redirect to Face Recognition page
            } else {
                setErrorMessage('Invalid username or password.');
            }
        } catch (err) {
            setErrorMessage('An unexpected error occurred: ' + err.message);
        }
    };

    return (
        <div className="login-container-modern">
            <h1>Welcome Back</h1>
            <form onSubmit={handleLogin} className="login-form-modern">
                <div className="form-group-modern">
                    <label htmlFor="username">University ID</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Enter your University ID"
                        required
                    />
                </div>
                <div className="form-group-modern">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />
                </div>
                <button type="submit" className="login-btn-modern">Log In</button>
                {errorMessage && <p className="error-message-modern">{errorMessage}</p>}
            </form>
        </div>
    );
};

export default LoginPage;
