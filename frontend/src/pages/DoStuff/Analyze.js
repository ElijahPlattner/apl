import React, { useEffect, useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';

import ListButton from './List_Button.js';

// Add a simple modal component
const HelpModal = ({ show, onClose }) => (
    show ? (
        <div
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100vw',
                height: '100vh',
                background: 'rgba(0,0,0,0.3)',
                zIndex: 9999,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            }}
            onClick={onClose}
        >
            <div
                style={{
                    background: '#fff',
                    borderRadius: '10px',
                    padding: '2rem',
                    maxWidth: '600px',
                    boxShadow: '0 2px 16px rgba(0,0,0,0.15)',
                    color: '#333'
                }}
                onClick={e => e.stopPropagation()}
            >
                <h3 style={{ marginBottom: '1rem' }}>How to use:</h3>
                <ul style={{ paddingLeft: '1.2rem', marginBottom: 0 }}>
                    <li>Use <b>Arrow Up</b> and <b>Arrow Down</b> keys to move between words in a column.</li>
                    <li>Click a word or right-click to start keyboard navigation from that word.</li>
                    <li>Press <b>F</b> while a word is focused or hovered to flag/unflag it.</li>
                    <li>Flagged words are highlighted in pink when active, and red when idle.</li>
                    <li>Hover over a word and right-click to focus it for keyboard navigation.</li>
                </ul>
                <div className="d-flex justify-content-end mt-4">
                    <button className="btn btn-primary" onClick={onClose}>Close</button>
                </div>
            </div>
        </div>
    ) : null
);



const Analyze = ({ setShowCreditsModal, setContentOpen }) => {

    const [fileContent, setFileContent] = useState('');
    const [analyzeStageController, setAnalyzeStageController] = useState("FileUpload"); //FileUpload, PreviewResults, FullResults
    const [focusedIdxCol1, setFocusedIdxCol1] = useState(0);
    const [focusedIdxCol2, setFocusedIdxCol2] = useState(0);
    const buttonRefsCol1 = useRef([]);
    const buttonRefsCol2 = useRef([]);
    const [showHelpModal, setShowHelpModal] = useState(false);

    useEffect(() => {
        if (buttonRefsCol1.current[focusedIdxCol1]) {
            buttonRefsCol1.current[focusedIdxCol1].focus();
        }
    }, [focusedIdxCol1]);

    useEffect(() => {
        if (buttonRefsCol2.current[focusedIdxCol2]) {
            buttonRefsCol2.current[focusedIdxCol2].focus();
        }
    }, [focusedIdxCol2]);

    const handleUpload = () => {
        const formData = new FormData();
        // If you only want to send the first file:
        if (acceptedFiles.length > 0) {
            formData.append('file', acceptedFiles[0], acceptedFiles[0].name); // 'file' is the field name
        }

        fetch('http://127.0.0.1:8000/api/upload/', {
            method: 'POST',
            body: formData,
            // Do NOT set Content-Type header; browser sets it for FormData
        })
            .then(response => response.json())
            .then(data => {
                // handle response
            })
            .catch(error => {
                // handle error
            });
    };

    useEffect(() => {
        fetch(process.env.PUBLIC_URL + '/react_log_001.txt')
            .then(response => response.text())
            .then(text => setFileContent(text));
    }, []);

    const {
        acceptedFiles,
        fileRejections,
        getRootProps,
        getInputProps
    } = useDropzone({
        accept: {
            'application/pdf': []
        },
        onDrop: acceptedFiles => {
            //do stuff with files
        }
    });

    const acceptedFileItems = acceptedFiles.map(file => (
        <li key={file.path}>
            {file.path} - {file.size} bytes
        </li>
    ));

    const fileRejectionItems = fileRejections.map(({ file, errors }) => (
        <li key={file.path}>
            {file.path} - {file.size} bytes
            <ul>
                {errors.map(e => (
                    <li key={e.code}>{e.message}</li>
                ))}
            </ul>
        </li>
    ));

    //const bunchOWords = Array.from({ length: 10 }).map(() => 'lorem').join(' ');
    const bunchOWords = ["Hello", "world!", "This", "is", "a", "list", "of", "words", "to", "display."].join(' ');
    const bunchOWords2 = ["Hello", "world!", "This", "is", "a", "list", "of", "words", "to", "display."].join(' ');

    const handleKeyDownCol1 = (e) => {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setFocusedIdxCol1(prev => Math.min(prev + 1, bunchOWords.split(' ').length - 1));
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setFocusedIdxCol1(prev => Math.max(prev - 1, 0));
        }
    };

    const handleKeyDownCol2 = (e) => {
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setFocusedIdxCol2(prev => Math.min(prev + 1, bunchOWords2.split(' ').length - 1));
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setFocusedIdxCol2(prev => Math.max(prev - 1, 0));
        }
    };

    return (
        <>
            <HelpModal show={showHelpModal} onClose={() => setShowHelpModal(false)} />
            <div className="card m-4 p-4 shadow-sm d-flex justify-content-center align-items-center" style={{ background: '#fff', borderRadius: '8px', minHeight: '400px' }}>
                {analyzeStageController === "FileUpload" ? (
                    <div className="d-flex flex-column align-items-center w-100">
                        <div className="d-flex flex-column">
                            <div className="d-flex flex-column align-items-start">
                                <section className="DragNDrop w-100">
                                    <div {...getRootProps({ className: 'dropzone' })}>
                                        <input {...getInputProps()} />
                                        <p>Drop Files here or click upload button to select files</p>
                                        <button className="btn btn-primary mb-3" type="button">
                                            <i className="bi bi-upload me-2"></i>Upload
                                        </button>
                                    </div>
                                </section>
                                {(acceptedFiles.length > 0 || fileRejections.length > 0) && (
                                    <>
                                        <h2 className="mt-4">Files</h2>
                                        <ul>
                                            {acceptedFiles.length > 0
                                                ? acceptedFileItems
                                                : <li style={{ color: '#888' }}>No accepted files added.</li>
                                            }
                                        </ul>
                                        {fileRejections.length > 0 && (
                                            <>
                                                <h2 className="mt-4" style={{ color: 'red' }}>Rejected Files</h2>
                                                <ul>{fileRejectionItems}</ul>
                                            </>
                                        )}

                                    </>
                                )}
                            </div>
                            {acceptedFiles.length > 0 && (
                                <div className="d-flex flex-column align-items-center">
                                    <button className="btn btn-success mt-3" type="button" onClick={() => setAnalyzeStageController("PreviewResults")}>
                                        <i className="bi bi-check-circle me-2"></i>Analyze
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                ) : analyzeStageController === "PreviewResults" ? (
                    <div className="d-flex flex-column align-items-center">
                        <h2 className="mt-4">We've Found du du du du du Results.</h2>
                        <div
                            style={{
                                background: '#f8f9fa',
                                padding: '1rem',
                                borderRadius: '8px',
                                maxHeight: '300px',
                                overflow: 'auto',
                                width: '100%',
                                fontFamily: 'monospace',
                                position: 'relative',
                                userSelect: 'none', // Prevent text selection
                                pointerEvents: 'none' // Prevent mouse events
                            }}
                        >
                            {Array.from({ length: 10 }).map((_, i) => {
                                const start = i * 100;
                                const end = start + 100;
                                const blur = i * 0.5;
                                return (
                                    <span
                                        key={i}
                                        style={{
                                            display: 'block',
                                            filter: `blur(${blur}px)`,
                                            opacity: 1 - i * 0.07,
                                            pointerEvents: 'none',
                                            userSelect: 'none'
                                        }}
                                    >
                                        {fileContent.slice(start, end)}
                                    </span>
                                );
                            })}
                        </div>
                        <div style={{ color: '#888', marginTop: '1rem', fontStyle: 'italic' }}>
                            To view full results will cost 1x Credit.
                        </div>
                        <div className='d-flex justify-content-center align-items-center'>
                            <button className="btn btn-primary mt-3" type="button" onClick={() => (console.log("pay for results"))}>
                                Purchase Results
                            </button>
                            <button
                                className="btn btn-primary mt-3 ms-3"
                                type="button"
                                onClick={() => setShowCreditsModal(true)}
                            >
                                Purchase Credits
                            </button>
                        </div>
                    </div>
                ) : analyzeStageController === "FullResults" ? (
                    <div className="d-flex flex-column align-items-center" style={{ position: 'relative', width: '100%' }}>
                        <div style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative' }}>
                            <h2 className="mt-4" style={{ padding: '2rem 1rem', marginBottom: 0, textAlign: 'center' }}>Full Results:</h2>
                            {/* Help button in top right */}
                            <button
                                type="button"
                                aria-label="Help"
                                style={{
                                    position: 'absolute',
                                    right: '1.5rem',
                                    top: '2.5rem',
                                    background: 'none',
                                    border: 'none',
                                    cursor: 'pointer',
                                    padding: 0,
                                    outline: 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    zIndex: 2
                                }}
                                onClick={() => setShowHelpModal(true)}
                            >
                                <span
                                    style={{
                                        display: 'inline-block',
                                        width: '28px',
                                        height: '28px',
                                        borderRadius: '50%',
                                        background: '#5bc0f7',
                                        color: '#fff',
                                        fontWeight: 'bold',
                                        fontSize: '1.5rem',
                                        textAlign: 'center',
                                        lineHeight: '28px',
                                        boxShadow: '0 1px 4px rgba(0,0,0,0.10)'
                                    }}
                                >?</span>
                            </button>
                        </div>
                        <div style={{ display: 'flex', gap: '2rem' }}>
                            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                                {bunchOWords.split(' ').map((word, idx) => (
                                    <li key={idx} style={{ marginBottom: '0.5rem' }}>
                                        <ListButton
                                            ref={el => buttonRefsCol1.current[idx] = el}
                                            tabIndex={0}
                                            text={word}
                                            item={word}
                                            onFlag={(flaggedWord) => {
                                                // Add your logic here, e.g. add flaggedWord to a flagged list
                                                console.log('Flagged:', flaggedWord);
                                            }}
                                            onKeyDown={handleKeyDownCol1}
                                            isFocused={focusedIdxCol1 === idx}
                                            onClick={() => setFocusedIdxCol1(idx)}
                                            setFocusIndex={() => setFocusedIdxCol1(idx)}
                                        />
                                    </li>
                                ))}
                            </ul>
                            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                                {bunchOWords2.split(' ').map((word, idx) => (
                                    <li key={idx} style={{ marginBottom: '0.5rem' }}>
                                        <ListButton
                                            ref={el => buttonRefsCol2.current[idx] = el}
                                            tabIndex={0}
                                            text={word}
                                            item={word}
                                            onFlag={(flaggedWord) => {
                                                // Add your logic here, e.g. add flaggedWord to a flagged list
                                                console.log('Flagged:', flaggedWord);
                                            }}
                                            onKeyDown={handleKeyDownCol2}
                                            isFocused={focusedIdxCol2 === idx}
                                            onClick={() => setFocusedIdxCol2(idx)}
                                            setFocusIndex={() => setFocusedIdxCol2(idx)}
                                        />
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : (
                    <div>You Broke It Refresh the Page Dummy</div>
                )}
            </div>

            <div className="d-flex justify-content-center align-items-center my-3" style={{ gap: '1rem' }}>
                <button
                    className="btn btn-outline-primary"
                    type="button"
                    onClick={() => setAnalyzeStageController("FileUpload")}
                >
                    File Upload
                </button>
                <button
                    className="btn btn-outline-primary"
                    type="button"
                    onClick={() => setAnalyzeStageController("PreviewResults")}
                >
                    Preview Results
                </button>
                <button
                    className="btn btn-outline-primary"
                    type="button"
                    onClick={() => setAnalyzeStageController("FullResults")}
                >
                    Full Results
                </button>
            </div>
        </>
    );
};



export default Analyze;