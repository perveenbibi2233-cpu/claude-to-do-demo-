import Icon from './Icon.jsx';
import { PRIORITIES, PRIORITY_LABELS } from '../utils/tasks.js';

function StatCard({ icon, label, value, tone }) {
  return (
    <div className={`stat-card tone-${tone}`}>
      <span className="stat-icon">
        <Icon name={icon} size={18} />
      </span>
      <div>
        <p className="stat-value" data-testid={`stat-${label.toLowerCase()}`}>
          {value}
        </p>
        <p className="stat-label">{label}</p>
      </div>
    </div>
  );
}

function ProgressRing({ percent }) {
  const r = 42;
  const c = 2 * Math.PI * r;
  return (
    <div className="ring" role="img" aria-label={`${percent}% of tasks completed`}>
      <svg viewBox="0 0 100 100" width="112" height="112">
        <circle className="ring-track" cx="50" cy="50" r={r} />
        <circle
          className="ring-fill"
          cx="50"
          cy="50"
          r={r}
          strokeDasharray={c}
          strokeDashoffset={c - (percent / 100) * c}
        />
      </svg>
      <div className="ring-label">
        <strong>{percent}%</strong>
        <span>done</span>
      </div>
    </div>
  );
}

export default function StatsDashboard({ stats }) {
  const message =
    stats.total === 0
      ? 'Add your first task to get started.'
      : stats.active === 0
        ? 'Everything is done. Nice work!'
        : `${stats.active} task${stats.active === 1 ? '' : 's'} left to go.`;

  return (
    <section className="dashboard" aria-label="Task statistics">
      <div className="card progress-card">
        <ProgressRing percent={stats.completionRate} />
        <div className="progress-text">
          <h2>Your progress</h2>
          <p>{message}</p>
          <div className="priority-bars">
            {PRIORITIES.map((p) => {
              const { total, completed } = stats.byPriority[p];
              const pct = total === 0 ? 0 : (completed / total) * 100;
              return (
                <div key={p} className="priority-bar">
                  <div className="priority-bar-head">
                    <span className={`dot dot-${p}`} />
                    <span>{PRIORITY_LABELS[p]}</span>
                    <span className="muted">
                      {completed}/{total}
                    </span>
                  </div>
                  <div className="bar">
                    <div className={`bar-fill fill-${p}`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      <div className="stat-grid">
        <StatCard icon="list" label="Total" value={stats.total} tone="indigo" />
        <StatCard icon="clock" label="Active" value={stats.active} tone="amber" />
        <StatCard icon="done" label="Completed" value={stats.completed} tone="green" />
        <StatCard icon="alert" label="Overdue" value={stats.overdue} tone="red" />
      </div>
    </section>
  );
}
