import { useEffect, useRef, useState } from 'react';
import Icon from './Icon.jsx';
import PrioritySelect from './PrioritySelect.jsx';
import { PRIORITY_LABELS, formatDueDate, isOverdue } from '../utils/tasks.js';

export default function TaskItem({ task, onToggle, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false);
  const [removing, setRemoving] = useState(false);
  const [draft, setDraft] = useState(task);
  const inputRef = useRef(null);
  const deletedRef = useRef(false);
  const timerRef = useRef(null);

  useEffect(() => () => clearTimeout(timerRef.current), []);

  const finishDelete = () => {
    if (deletedRef.current) return;
    deletedRef.current = true;
    clearTimeout(timerRef.current);
    onDelete(task.id);
  };

  useEffect(() => {
    if (editing) {
      inputRef.current?.focus();
      inputRef.current?.select();
    }
  }, [editing]);

  const startEdit = () => {
    setDraft({ title: task.title, priority: task.priority, dueDate: task.dueDate });
    setEditing(true);
  };

  const save = () => {
    if (!draft.title.trim()) return;
    onUpdate(task.id, {
      title: draft.title,
      priority: draft.priority,
      dueDate: draft.dueDate,
    });
    setEditing(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      save();
    } else if (e.key === 'Escape') {
      setEditing(false);
    }
  };

  const handleDelete = () => {
    if (removing) return;
    setRemoving(true);
    // Fallback in case the exit animation doesn't run (reduced motion, background tab).
    timerRef.current = setTimeout(finishDelete, 400);
  };

  const overdue = isOverdue(task);

  if (editing) {
    return (
      <li className={`task-item editing prio-${draft.priority}`}>
        <div className="edit-body">
          <input
            ref={inputRef}
            className="edit-input"
            value={draft.title}
            onChange={(e) => setDraft({ ...draft, title: e.target.value })}
            onKeyDown={handleKeyDown}
            aria-label="Edit task title"
            maxLength={200}
          />
          <div className="edit-options">
            <PrioritySelect
              value={draft.priority}
              onChange={(p) => setDraft({ ...draft, priority: p })}
              name={`priority-${task.id}`}
              compact
            />
            <label className="date-field compact">
              <Icon name="calendar" size={15} />
              <input
                type="date"
                value={draft.dueDate}
                onChange={(e) => setDraft({ ...draft, dueDate: e.target.value })}
                aria-label="Edit due date"
              />
            </label>
            <div className="edit-actions">
              <button type="button" className="btn btn-ghost" onClick={() => setEditing(false)}>
                Cancel
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={save}
                disabled={!draft.title.trim()}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      </li>
    );
  }

  return (
    <li
      className={`task-item prio-${task.priority} ${task.completed ? 'completed' : ''} ${
        removing ? 'removing' : ''
      }`}
      onAnimationEnd={(e) => {
        if (removing && e.animationName === 'item-out') finishDelete();
      }}
    >
      <button
        type="button"
        className={`checkbox ${task.completed ? 'checked' : ''}`}
        onClick={() => onToggle(task.id)}
        role="checkbox"
        aria-checked={task.completed}
        aria-label={`Mark "${task.title}" as ${task.completed ? 'not completed' : 'completed'}`}
      >
        <Icon name="check" size={14} strokeWidth={3} />
      </button>

      <div className="task-body" onDoubleClick={startEdit}>
        <p className="task-title">{task.title}</p>
        <div className="task-meta">
          <span className={`badge badge-${task.priority}`}>
            <span className={`dot dot-${task.priority}`} />
            {PRIORITY_LABELS[task.priority]}
          </span>
          {task.dueDate && (
            <span className={`badge badge-date ${overdue ? 'overdue' : ''}`}>
              <Icon name={overdue ? 'alert' : 'calendar'} size={12} />
              {overdue ? 'Overdue · ' : ''}
              {formatDueDate(task.dueDate)}
            </span>
          )}
        </div>
      </div>

      <div className="task-actions">
        <button
          type="button"
          className="icon-btn"
          onClick={startEdit}
          aria-label={`Edit "${task.title}"`}
          title="Edit"
        >
          <Icon name="edit" size={17} />
        </button>
        <button
          type="button"
          className="icon-btn danger"
          onClick={handleDelete}
          aria-label={`Delete "${task.title}"`}
          title="Delete"
        >
          <Icon name="trash" size={17} />
        </button>
      </div>
    </li>
  );
}
