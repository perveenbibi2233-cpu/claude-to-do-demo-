import { useCallback, useMemo, useState } from 'react';
import Header from './components/Header.jsx';
import StatsDashboard from './components/StatsDashboard.jsx';
import TaskForm from './components/TaskForm.jsx';
import Toolbar from './components/Toolbar.jsx';
import TaskItem from './components/TaskItem.jsx';
import EmptyState from './components/EmptyState.jsx';
import Toast from './components/Toast.jsx';
import { useTasks } from './hooks/useTasks.js';
import { useTheme } from './hooks/useTheme.js';
import { filterTasks, getStats, sortTasks } from './utils/tasks.js';

const DEFAULT_FILTERS = { search: '', status: 'all', priority: 'all', sort: 'newest' };

export default function App() {
  const { tasks, addTask, updateTask, toggleTask, deleteTask, restoreTask, clearCompleted } =
    useTasks();
  const { theme, toggleTheme } = useTheme();
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [toast, setToast] = useState(null);

  const stats = useMemo(() => getStats(tasks), [tasks]);

  // Status-tab counts respect the search and priority filters so the numbers match the list.
  const counts = useMemo(() => {
    const base = filterTasks(tasks, { ...filters, status: 'all' });
    const completed = base.filter((t) => t.completed).length;
    return { all: base.length, active: base.length - completed, completed };
  }, [tasks, filters]);

  const visibleTasks = useMemo(
    () => sortTasks(filterTasks(tasks, filters), filters.sort),
    [tasks, filters]
  );

  const handleDelete = useCallback(
    (id) => {
      const index = tasks.findIndex((t) => t.id === id);
      if (index === -1) return;
      const task = tasks[index];
      deleteTask(id);
      setToast({
        key: Date.now(),
        message: `Deleted "${task.title.length > 32 ? task.title.slice(0, 32) + '…' : task.title}"`,
        undo: () => restoreTask(task, index),
      });
    },
    [tasks, deleteTask, restoreTask]
  );

  const handleClearCompleted = () => {
    const removed = tasks.filter((t) => t.completed).length;
    if (removed === 0) return;
    const snapshot = tasks;
    clearCompleted();
    setToast({
      key: Date.now(),
      message: `Cleared ${removed} completed task${removed === 1 ? '' : 's'}`,
      undo: () => snapshot.forEach((t, i) => t.completed && restoreTask(t, i)),
    });
  };

  const closeToast = useCallback(() => setToast(null), []);
  const filtersActive =
    filters.search !== '' || filters.status !== 'all' || filters.priority !== 'all';

  return (
    <div className="app">
      <div className="bg-glow" aria-hidden="true" />
      <main className="container">
        <Header theme={theme} onToggleTheme={toggleTheme} />
        <StatsDashboard stats={stats} />
        <TaskForm onAdd={addTask} />

        <section className="card tasks-card" aria-label="Tasks">
          <Toolbar filters={filters} onChange={setFilters} counts={counts} />

          {visibleTasks.length === 0 ? (
            <EmptyState hasTasks={tasks.length > 0} onReset={() => setFilters(DEFAULT_FILTERS)} />
          ) : (
            <ul className="task-list">
              {visibleTasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggle={toggleTask}
                  onUpdate={updateTask}
                  onDelete={handleDelete}
                />
              ))}
            </ul>
          )}

          {tasks.length > 0 && (
            <footer className="tasks-footer">
              <span className="muted">
                Showing {visibleTasks.length} of {tasks.length}
                {filtersActive ? ' (filtered)' : ''}
              </span>
              <button
                type="button"
                className="link-btn"
                onClick={handleClearCompleted}
                disabled={stats.completed === 0}
              >
                Clear completed
              </button>
            </footer>
          )}
        </section>

        <p className="hint">Tip: double-click a task to edit it. Tasks are saved in your browser.</p>
      </main>

      {toast && (
        <Toast
          key={toast.key}
          message={toast.message}
          actionLabel="Undo"
          onAction={() => {
            toast.undo();
            setToast(null);
          }}
          onClose={closeToast}
        />
      )}
    </div>
  );
}
