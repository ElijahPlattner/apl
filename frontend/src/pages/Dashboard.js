import React, { useEffect, useState, useRef } from 'react';
//content imports
import Analyze from './DoStuff/Analyze.js';
import History from './DoStuff/History.js';
import PurchaseCreditsModal from './PurchaseCreditsModal.js';

const DoStuff = () => {
    const [contentOpen, setContentOpen] = React.useState("Analyze");
    const [showProfileMenu, setShowProfileMenu] = React.useState(false);
    const profileMenuRef = useRef(null);
    const profileButtonRef = useRef(null);
    const [sidebarExpanded, setSidebarExpanded] = React.useState(true);
    const [showCreditsModal, setShowCreditsModal] = useState(false);

    useEffect(() => {
        function handleClickOutside(event) {
            if (
                profileMenuRef.current &&
                !profileMenuRef.current.contains(event.target) &&
                profileButtonRef.current &&
                !profileButtonRef.current.contains(event.target)
            ) {
                setShowProfileMenu(false);
            }
        }
        if (showProfileMenu) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [showProfileMenu]);

    const handleAnalyzeClick = () => {
        setContentOpen("Analyze");
    };

    const handleHistoryClick = () => {
        setContentOpen("History");
    };

    return (
        <>
            <nav className="navbar px-4">
                <div className="d-flex flex-row justify-content-between align-items-center w-100">
                    <div className="d-flex flex-row">
                        {sidebarExpanded && (
                            <span
                                style={{
                                    color: '#fff',
                                    fontSize: '2rem',
                                    fontWeight: 'bold',
                                    marginRight: '1.5rem',
                                    letterSpacing: '1px',
                                    transition: 'opacity 0.3s',
                                    opacity: sidebarExpanded ? 1 : 0,
                                }}
                            >
                                APL Dashboard
                            </span>
                        )}
                        <button
                            className="btn btn-link text-white me-3"
                            style={{ fontSize: '1.5rem', paddingLeft: 0, paddingRight: 0 }}
                            onClick={() => setSidebarExpanded(!sidebarExpanded)}
                            aria-label={sidebarExpanded ? "Collapse sidebar" : "Expand sidebar"}
                        >
                            <i className={`bi ${sidebarExpanded ? "bi-chevron-left" : "bi-list"}`}></i>
                        </button>

                    </div>

                    <div className="d-flex flex-row align-items-center" style={{ position: 'relative' }}>
                        <button className="btn btn-primary me-3" onClick={() => setShowCreditsModal(true)}>
                            Purchase Credits
                        </button>
                        <span className="navbar-text mx-3">
                            Credits : Gazillions
                        </span>
                        <button
                            ref={profileButtonRef}
                            className="profile-pic d-flex align-items-center justify-content-center rounded-circle bg-light border"
                            style={{ width: '40px', height: '40px', border: 'none', cursor: 'pointer' }}
                            onClick={() => setShowProfileMenu((open) => !open)}
                            aria-label="Profile"
                        >
                            <i className="bi bi-person" style={{ fontSize: '1.5rem', color: '#5865F2' }}></i>
                        </button>
                        {showProfileMenu && (
                            <div
                                ref={profileMenuRef}
                                className="dropdown-menu show"
                                style={{ position: 'absolute', right: 0, top: '48px', minWidth: '140px', zIndex: 1000 }}
                            >
                                <button className="dropdown-item" onClick={() => alert('Profile clicked!')}>Profile</button>
                                <button className="dropdown-item" onClick={() => alert('Settings clicked!')}>Settings</button>
                                <button className="dropdown-item" onClick={() => alert('Logout clicked!')}>Logout</button>
                            </div>
                        )}
                    </div>
                </div>
            </nav>

            <div className="d-flex" style={{ minHeight: 'calc(100vh - 56px)' }}>

                <aside className={`sidebar sidebar-default sidebar-white sidebar-base navs-rounded-all ${sidebarExpanded ? 'expanded' : 'collapsed'}`}>
                    <div className="sidebar-body pt-0 data-scrollbar" style={{ overflowY: "auto", outline: "none", flex: 1 }}>
                        <ul className="navbar-nav iq-main-menu" id="sidebar-menu">
                            {/* Category Title */}
                            {sidebarExpanded && (
                                <li className="nav-item static-item" style={{ padding: '0.5rem 0', fontWeight: 'bold', color: '#1d9b36', fontSize: '1.1rem', letterSpacing: '1px' }}>
                                    <span className="default-icon">Tools</span>
                                </li>
                            )}
                            {/* Nav Items */}
                            <li className={`nav-item${contentOpen === "Analyze" ? " active" : ""}`}>
                                <a className="nav-link" onClick={handleAnalyzeClick} style={{ justifyContent: 'center', display: 'flex', alignItems: 'center' }}>
                                    <i className="bi bi-search me-2"></i>
                                    {sidebarExpanded && <span className="item-name">Analyze</span>}
                                </a>
                            </li>
                            <li className={`nav-item${contentOpen === "History" ? " active" : ""}`}>
                                <a className="nav-link" onClick={handleHistoryClick} style={{ justifyContent: 'center', display: 'flex', alignItems: 'center' }}>
                                    <i className="bi bi-download me-2"></i>
                                    {sidebarExpanded && <span className="item-name">History</span>}
                                </a>
                            </li>
                        </ul>
                    </div>
                </aside>

                <div className="main-content" style={{ flex: 1, padding: '2rem' }}>
                    {
                        contentOpen === "Analyze" ? (
                            <Analyze setShowCreditsModal={setShowCreditsModal} setContentOpen={setContentOpen} />
                        ) : contentOpen === "History" ? (
                            <History setShowCreditsModal={setShowCreditsModal} setContentOpen={setContentOpen} />
                        ) : (
                            <div className="container mt-4">
                                <h2>Some thing bad happened</h2>
                            </div>
                        )
                    }
                </div>
            </div>
            <PurchaseCreditsModal show={showCreditsModal} onClose={() => setShowCreditsModal(false)} />
        </>
    );
};

export default DoStuff;