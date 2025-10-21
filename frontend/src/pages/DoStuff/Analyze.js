import React, { useEffect, useState } from 'react';
import { useDropzone } from 'react-dropzone';


const Analyze = ({ setShowTokensModal }) => {

    const [fileContent, setFileContent] = useState('');
    const [showPreview, setShowPreview] = useState("false");


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
            'text/plain': [],
            'application/pdf': []
        },
        onDrop: acceptedFiles => {
            //do stuuff with files
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

    return (
        <div className="card m-4 p-4 shadow-sm d-flex justify-content-center align-items-center" style={{ background: '#fff', borderRadius: '8px', minHeight: '400px' }}>
            {showPreview === "false" ? (
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
                                <button className="btn btn-success mt-3" type="button" onClick={() => setShowPreview("true")}>
                                    <i className="bi bi-check-circle me-2"></i>Analyze
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            ) : (
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
                        To view full results will cost 1x token.
                    </div>
                    <div className='d-flex justify-content-center align-items-center'>
                        <button className="btn btn-primary mt-3" type="button" onClick={() => (console.log("pay for results"))}>
                            Purchase Results
                        </button>
                        <button
                            className="btn btn-primary mt-3 ms-3"
                            type="button"
                            onClick={() => setShowTokensModal(true)}
                        >
                            Purchase Tokens
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Analyze;