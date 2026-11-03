import { useState } from 'react';
import Icon from './Icon.jsx';
import PrioritySelect from './PrioritySelect.jsx';

export default function TaskForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('medium');
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Please enter a task title.');
      return;
    }
    onAdd({ title, priority, dueDate });
    setTitle('');
    setDueDate('');
    setError('');
  };

  return (
    <form className="card task-form" onSubmit={handleSubmit} noValidate>
      <div className={`input-row ${error ? 'has-error' : ''}`}>
        <input
          className="task-input"
          type="text"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            if (error) setError('');
          }}
          placeholder="What needs to be done?"
          aria-label="New task title"
          aria-invalid={Boolean(error)}
          aria-describedby={error ? 'task-error' : undefined}
          maxLength={200}
        />
        <button type="submit" className="btn btn-primary add-btn" aria-label="Add task">
          <Icon name="plus" size={18} strokeWidth={2.5} />
          <span>Add task</span>
        </button>
      </div>
      {error && (
        <p id="task-error" className="form-error" role="alert">
          {error}
        </p>
      )}
      <div className="form-options">
        <PrioritySelect value={priority} onChange={setPriority} name="new-priority" />
        <label className="date-field">
          <Icon name="calendar" size={16} />
          <span className="sr-only">Due date</span>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            aria-label="Due date"
          />
        </label>
      </div>
    </form>
  );
}
