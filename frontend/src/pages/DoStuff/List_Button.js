import React, { useState, useRef, useEffect } from 'react';

const ListButton = ({ text, item, onFlag }) => {
    const [flagged, setFlagged] = useState(false);
    const [hovered, setHovered] = useState(false);
    const buttonRef = useRef(null);

    // Handle flag click (now used for all button clicks)
    const handleFlagClick = (e) => {
        // Remove e.stopPropagation so parent button also gets the event
        setFlagged((prev) => {
            onFlag(item);
            return !prev;
        });
    };

    // Listen for global keydown when hovered
    useEffect(() => {
        if (!hovered) return;
        const handleGlobalKeyDown = (e) => {
            if (e.key.toLowerCase() === 'f') {
                setFlagged((prev) => {
                    onFlag(item);
                    return !prev;
                });
            }
        };
        window.addEventListener('keydown', handleGlobalKeyDown);
        return () => {
            window.removeEventListener('keydown', handleGlobalKeyDown);
        };
    }, [hovered, item, onFlag]);

    return (
        <button
            className={`btn btn-listbutton d-flex align-items-center justify-content-center ${flagged ? 'flagged' : ''}`}
            tabIndex={0}
            ref={buttonRef}
            type="button"
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            onClick={handleFlagClick} // <-- handle click for entire button
        >
            <button
                className="flag-btn"
                // Remove onClick here so parent handles it
                type="button"
                aria-label={flagged ? "Unflag item" : "Flag item"}
                tabIndex={-1} // Remove from tab order, since parent is focusable
                style={{
                    border: 'none',
                    outline: 'none',
                    background: 'none',
                    padding: 0,
                    marginRight: '0.5rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}
            >
                <span className="flag-btn-circle">
                    <i className={`bi bi-flag${flagged ? '-fill' : ''}`}></i>
                </span>
            </button>
            <span style={{
                width: '1px',
                background: '#ccc',
                alignSelf: 'stretch',
            }} />
            <span style={{ flex: 1, minWidth: '80px', textAlign: 'center', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>{text}</span>
        </button>
    );
};

export default ListButton;