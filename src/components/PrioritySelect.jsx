import { PRIORITIES, PRIORITY_LABELS } from '../utils/tasks.js';

export default function PrioritySelect({ value, onChange, name = 'priority', compact = false }) {
  return (
    <div
      className={`segmented ${compact ? 'compact' : ''}`}
      role="radiogroup"
      aria-label="Priority"
    >
      {PRIORITIES.map((p) => (
        <label key={p} className={`segment seg-${p} ${value === p ? 'selected' : ''}`}>
          <input
            type="radio"
            name={name}
            value={p}
            checked={value === p}
            onChange={() => onChange(p)}
          />
          <span className={`dot dot-${p}`} />
          {PRIORITY_LABELS[p]}
        </label>
      ))}
    </div>
  );
}
