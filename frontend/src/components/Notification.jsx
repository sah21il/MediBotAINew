import { useState, useEffect } from 'react';

export default function Notification({ message, type, onClose }) {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        onClose();
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [message, onClose]);

  if (!message) return null;

  const colors = {
    success: { bg: '#27ae60', border: '#2ecc71' },
    error: { bg: '#e74c3c', border: '#c0392b' },
    warning: { bg: '#f39c12', border: '#e67e22' },
    info: { bg: '#3498db', border: '#2980b9' }
  };

  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  };

  return (
    <div style={{
      position: 'fixed',
      top: '20px',
      right: '20px',
      zIndex: 10000,
      animation: 'slideIn 0.3s ease-out'
    }}>
      <div style={{
        background: colors[type].bg,
        border: `2px solid ${colors[type].border}`,
        borderRadius: '12px',
        padding: '16px 24px',
        minWidth: '300px',
        maxWidth: '500px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <span style={{ fontSize: '24px' }}>{icons[type]}</span>
        <div style={{ flex: 1, color: 'white', fontSize: '15px', fontWeight: '500' }}>
          {message}
        </div>
        <button
          onClick={onClose}
          style={{
            background: 'rgba(255,255,255,0.2)',
            border: 'none',
            color: 'white',
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            cursor: 'pointer',
            fontSize: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          ×
        </button>
      </div>
      <style>{`
        @keyframes slideIn {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
}

export function ConfirmDialog({ message, onConfirm, onCancel }) {
  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0,0,0,0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 10000,
      animation: 'fadeIn 0.2s ease-out'
    }}>
      <div style={{
        background: '#2d2d2d',
        borderRadius: '15px',
        padding: '30px',
        minWidth: '400px',
        border: '1px solid rgba(255,255,255,0.1)',
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
        animation: 'scaleIn 0.2s ease-out'
      }}>
        <div style={{ fontSize: '48px', textAlign: 'center', marginBottom: '20px' }}>
          ⚠️
        </div>
        <h3 style={{ color: '#e9ecef', textAlign: 'center', marginBottom: '20px', fontSize: '18px' }}>
          {message}
        </h3>
        <div style={{ display: 'flex', gap: '15px', marginTop: '30px' }}>
          <button
            onClick={onCancel}
            style={{
              flex: 1,
              padding: '12px',
              background: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            style={{
              flex: 1,
              padding: '12px',
              background: '#e74c3c',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            Delete
          </button>
        </div>
      </div>
      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scaleIn {
          from { transform: scale(0.9); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
