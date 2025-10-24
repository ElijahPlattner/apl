import React from 'react';
import { Modal } from 'react-bootstrap';

export function PurchaseCreditsModal({ show, onClose }) {
    return (
        <Modal show={show} onHide={onClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Purchase Credits</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {/* Your purchase credits UI here */}
                <p>Credits purchase functionality goes here.</p>
            </Modal.Body>
            <Modal.Footer>
                <button className="btn btn-secondary" onClick={onClose}>
                    Close
                </button>
            </Modal.Footer>
        </Modal>
    );
}

export default PurchaseCreditsModal;