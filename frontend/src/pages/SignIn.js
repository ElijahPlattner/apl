import React, { useState } from 'react';

function SignIn() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSignIn = () => {
        setError('');
        fetch('http://localhost:8000/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Invalid credentials');
                }
                return res.json();
            })
            .then(data => {
                if (data.access && data.refresh) {
                    localStorage.setItem('access', data.access);
                    localStorage.setItem('refresh', data.refresh);
                    window.location.href = '/DoStuff';
                } else {
                    throw new Error('Login failed');
                }
            })
            .catch(err => {
                setError('Sign in failed. Please check your username and password.');
            });
    };

    const handleRegisterClick = () => {
        window.location.href = '/Register';
    };

    return (
        <div className="d-flex justify-content-center align-items-center min-vh-100">
            <div className="card p-4 shadow" style={{ width: '600px' }}>
                <h2 className="mb-4 text-center">Sign In</h2>
                {error && <div className="alert alert-danger">{error}</div>}
                <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                        type="text"
                        className="form-control"
                        id="username"
                        placeholder="Enter your username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="password" className="form-label">Password</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />
                </div>
                <button className="btn btn-primary" onClick={handleSignIn}>Sign In</button>
                <div className="mt-3 text-center">
                    <span>No account? </span>
                    <span
                        style={{ color: '#5865F2', cursor: 'pointer', textDecoration: 'underline' }}
                        onClick={handleRegisterClick}
                    >
                        Register here
                    </span>
                </div>
            </div>
        </div>
    );
}

export default SignIn;

