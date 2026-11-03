import { useEffect } from 'react';

export default function Toast({ message, actionLabel, onAction, onClose, duration = 5000 }) {
  useEffect(() => {
    const id = setTimeout(onClose, duration);
    return () => clearTimeout(id);
  }, [message, onClose, duration]);

  return (
    <div className="toast" role="status">
      <span>{message}</span>
      {onAction && (
        <button type="button" className="toast-action" onClick={onAction}>
          {actionLabel}
        </button>
      )}
    </div>
  );
}
