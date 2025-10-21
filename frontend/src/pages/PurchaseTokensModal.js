import React from 'react';
import { Modal } from 'react-bootstrap';

export function PurchaseTokensModal({ show, onClose }) {
    return (
        <Modal show={show} onHide={onClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Purchase Tokens</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                {/* Your purchase tokens UI here */}
                <p>Token purchase functionality goes here.</p>
            </Modal.Body>
            <Modal.Footer>
                <button className="btn btn-secondary" onClick={onClose}>
                    Close
                </button>
            </Modal.Footer>
        </Modal>
    );
}

export default PurchaseTokensModal;