import React, { useState } from 'react';

function Register() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [error, setError] = useState('');

    const handleRegister = () => {
        setError('');
        fetch('http://127.0.0.1:8000/api/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                email,
                password,
                password2: passwordConfirm,
                first_name: firstName,
                last_name: lastName
            })
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(data => { throw new Error(data.password || data.email || 'Registration failed'); });
                }
                return res.json();
            })
            .then(data => {
                window.location.href = '/Dashboard';
            })
            .catch(err => {
                console.log('Registration error:', err.message); // Log error to console
                setError(err.message || 'Registration failed. Please check your details.');
            });
    };

    return (
        <div className="d-flex justify-content-center align-items-center min-vh-100">
            <div className="card p-4 shadow" style={{ width: '600px' }}>
                <h2 className="mb-4 text-center">Register</h2>
                {error && <div className="alert alert-danger">{error}</div>}
                {/* Username and Email stacked vertically */}
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
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                        type="email"
                        className="form-control"
                        id="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                </div>
                {/* First Name and Last Name in one row */}
                <div className="row mb-3">
                    <div className="col">
                        <label htmlFor="firstName" className="form-label">First Name</label>
                        <input
                            type="text"
                            className="form-control"
                            id="firstName"
                            placeholder="Enter your first name"
                            value={firstName}
                            onChange={e => setFirstName(e.target.value)}
                        />
                    </div>
                    <div className="col">
                        <label htmlFor="lastName" className="form-label">Last Name</label>
                        <input
                            type="text"
                            className="form-control"
                            id="lastName"
                            placeholder="Enter your last name"
                            value={lastName}
                            onChange={e => setLastName(e.target.value)}
                        />
                    </div>
                </div>
                {/* Password and Confirm Password in one row */}
                <div className="row mb-3">
                    <div className="col">
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
                    <div className="col">
                        <label htmlFor="passwordConfirm" className="form-label">Confirm Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="passwordConfirm"
                            placeholder="Confirm your password"
                            value={passwordConfirm}
                            onChange={e => setPasswordConfirm(e.target.value)}
                        />
                    </div>
                </div>
                <button className="btn btn-primary w-100" onClick={handleRegister}>Register</button>
                <div className="mt-3 text-center">
                    <span>Already have an account? </span>
                    <span
                        style={{ color: '#5865F2', cursor: 'pointer', textDecoration: 'underline' }}
                        onClick={() => window.location.href = '/signin'}
                    >
                        Sign in here
                    </span>
                </div>
            </div>
        </div>
    );
}

export default Register;