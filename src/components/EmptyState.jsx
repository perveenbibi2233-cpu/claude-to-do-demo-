import Icon from './Icon.jsx';

export default function EmptyState({ hasTasks, onReset }) {
  return (
    <div className="empty">
      <div className="empty-icon">
        <Icon name={hasTasks ? 'search' : 'sparkle'} size={28} />
      </div>
      <h3>{hasTasks ? 'No matching tasks' : 'No tasks yet'}</h3>
      <p>
        {hasTasks
          ? 'Try a different search or clear your filters.'
          : 'Add a task above to start planning your day.'}
      </p>
      {hasTasks && (
        <button type="button" className="btn btn-ghost" onClick={onReset}>
          Clear filters
        </button>
      )}
    </div>
  );
}
