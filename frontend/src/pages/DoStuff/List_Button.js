import React, { useState, forwardRef } from 'react';

const ListButton = forwardRef(({ text, item, onFlag, onKeyDown, onClick, setFocusIndex }, buttonRef) => {
    const [flagged, setFlagged] = useState(false);

    // Handle flag click (now used for all button clicks)
    const handleFlagClick = (e) => {
        setFlagged((prev) => {
            onFlag(item);
            return !prev;
        });
        if (onClick) onClick(e);
    };

    // Handle F key for flagging when button is focused
    const handleKeyDown = (e) => {
        if (e.key.toLowerCase() === 'f') {
            e.preventDefault();
            setFlagged((prev) => {
                onFlag(item);
                return !prev;
            });
        }
        if (onKeyDown) {
            onKeyDown(e);
        }
    };

    // Handle right-click to focus and prevent context menu
    const handleContextMenu = (e) => {
        e.preventDefault();
        if (buttonRef && buttonRef.current) {
            buttonRef.current.focus();
        }
        if (setFocusIndex) {
            setFocusIndex();
        }
    };

    return (
        <button
            className={`btn btn-listbutton d-flex align-items-center justify-content-center ${flagged ? 'flagged' : ''}`}
            tabIndex={0}
            ref={buttonRef}
            type="button"
            onClick={handleFlagClick}
            onKeyDown={handleKeyDown}
            onContextMenu={handleContextMenu}
        >
            <button
                className="flag-btn"
                type="button"
                aria-label={flagged ? "Unflag item" : "Flag item"}
                tabIndex={-1}
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
});

export default ListButton;