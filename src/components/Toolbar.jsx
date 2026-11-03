import Icon from './Icon.jsx';

const STATUS_OPTIONS = [
  { value: 'all', label: 'All' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' },
];

export default function Toolbar({ filters, onChange, counts }) {
  const set = (key) => (value) => onChange({ ...filters, [key]: value });

  return (
    <div className="toolbar">
      <div className="search">
        <Icon name="search" size={17} />
        <input
          type="search"
          placeholder="Search tasks…"
          value={filters.search}
          onChange={(e) => set('search')(e.target.value)}
          aria-label="Search tasks"
        />
        {filters.search && (
          <button
            type="button"
            className="search-clear"
            onClick={() => set('search')('')}
            aria-label="Clear search"
          >
            <Icon name="x" size={14} />
          </button>
        )}
      </div>

      <div className="toolbar-row">
        <div className="tabs" role="tablist" aria-label="Filter by status">
          {STATUS_OPTIONS.map((o) => (
            <button
              key={o.value}
              type="button"
              role="tab"
              aria-selected={filters.status === o.value}
              className={`tab ${filters.status === o.value ? 'active' : ''}`}
              onClick={() => set('status')(o.value)}
            >
              {o.label}
              <span className="tab-count">{counts[o.value]}</span>
            </button>
          ))}
        </div>

        <div className="selects">
          <select
            value={filters.priority}
            onChange={(e) => set('priority')(e.target.value)}
            aria-label="Filter by priority"
          >
            <option value="all">All priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
          <select
            value={filters.sort}
            onChange={(e) => set('sort')(e.target.value)}
            aria-label="Sort tasks"
          >
            <option value="newest">Newest first</option>
            <option value="oldest">Oldest first</option>
            <option value="priority">Priority</option>
            <option value="due">Due date</option>
          </select>
        </div>
      </div>
    </div>
  );
}
