//import React, { useRef, useEffect } from 'react';

const Landing = () => {
    return (
        <>
            <div
                className="min-vh-100 d-flex flex-column justify-content-center align-items-center"
                style={{
                    background: 'linear-gradient(135deg, #1d9b36 0%, #000000e9 100%)',
                    color: '#fff'
                }}
            >
                <h1 className="fw-bold display-3 mb-3" style={{ letterSpacing: '2px', color: '#fff' }}>
                    Welcome to APL!
                </h1>
                <p className="lead mb-4 text-center" style={{ maxWidth: '500px' }}>
                    Here is a lot of flavor text for the website. dont forget to change me later please!
                </p>
                <div className="my-4 d-flex justify-content-center gap-3">
                    <button
                        className="btn btn-primary"
                        style={{ minWidth: '140px' }}
                        onClick={() => window.location.href = '/signin'}
                    >
                        Sign In
                    </button>
                    <button
                        className="btn btn-secondary"
                        style={{ minWidth: '140px' }}
                        onClick={() => window.location.href = '/register'}
                    >
                        Register
                    </button>
                </div>
                <div
                    className="mt-5 p-4 rounded shadow align-self-center text-center"
                    style={{
                        background: '#fff',
                        color: '#23272A',
                        minWidth: '320px',
                        maxWidth: '400px',
                        boxShadow: '0 2px 16px rgba(35,39,42,0.10)'
                    }}
                >
                    <h2 className="mb-2" style={{ color: '#1d9b36' }}>Contact Us</h2>
                    <p className="mb-1">Email: <a href="mailto:contact@example.com" style={{ color: '#1d9b36', textDecoration: 'underline' }}>contact@example.com</a></p>
                    <p>Phone: <span style={{ color: '#1d9b36' }}>+1 (555) 123-4567</span></p>
                </div>
            </div>
        </>
    );
};

export default Landing;