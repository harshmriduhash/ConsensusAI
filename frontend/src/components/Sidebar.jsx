import { useState } from 'react';
import { api } from '../api';
import DeleteModal from './DeleteModal';
import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
}) {
  const [deleteModalOpen, setDeleteModalOpen] = useState(false);
  const [conversationToDelete, setConversationToDelete] = useState(null);

  const handleDeleteClick = (e, conversation) => {
    e.stopPropagation(); // Prevent selecting the conversation
    setConversationToDelete(conversation);
    setDeleteModalOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!conversationToDelete) return;

    try {
      await api.deleteConversation(conversationToDelete.id);
      setDeleteModalOpen(false);
      setConversationToDelete(null);
      // Refresh conversations list
      window.location.reload();
    } catch (error) {
      console.error('Failed to delete conversation:', error);
      setDeleteModalOpen(false);
      setConversationToDelete(null);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteModalOpen(false);
    setConversationToDelete(null);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1 className="app-title">ConsensusAI</h1>
        <p className="app-subtitle">AI Deliberation Platform</p>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Conversation
        </button>
      </div>

      <div className="conversations-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">
            <p>No conversations yet</p>
            <span>Start a new conversation to begin</span>
          </div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title">
                {conv.title || 'New Conversation'}
              </div>
              <div className="conversation-date">
                {formatDate(conv.created_at)}
              </div>
              <button
                className="delete-btn"
                onClick={(e) => handleDeleteClick(e, conv)}
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>

      <DeleteModal
        isOpen={deleteModalOpen}
        onClose={handleDeleteCancel}
        onConfirm={handleDeleteConfirm}
        conversationTitle={conversationToDelete?.title || 'New Conversation'}
      />
    </div>
  );
}
