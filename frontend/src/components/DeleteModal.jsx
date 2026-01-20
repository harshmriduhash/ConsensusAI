import "./DeleteModal.css";

export default function DeleteModal({
  isOpen,
  onClose,
  onConfirm,
  conversationTitle,
}) {
  if (!isOpen) return null;

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="modal-content">
        <div className="modal-icon">⚠️</div>
        <h2 className="modal-title">Delete Conversation?</h2>
        <p className="modal-message">
          Are you sure you want to delete "
          {conversationTitle || "this conversation"}"? This action cannot be
          undone.
        </p>
        <div className="modal-actions">
          <button className="modal-btn modal-btn-cancel" onClick={onClose}>
            Cancel
          </button>
          <button className="modal-btn modal-btn-delete" onClick={onConfirm}>
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}
