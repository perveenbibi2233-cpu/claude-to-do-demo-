export const PRIORITIES = ['high', 'medium', 'low'];

export const PRIORITY_LABELS = {
  high: 'High',
  medium: 'Medium',
  low: 'Low',
};

const PRIORITY_RANK = { high: 0, medium: 1, low: 2 };

export function createId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

export function createTask({ title, priority = 'medium', dueDate = '' }) {
  const now = new Date().toISOString();
  return {
    id: createId(),
    title: title.trim(),
    priority: PRIORITIES.includes(priority) ? priority : 'medium',
    dueDate: dueDate || '',
    completed: false,
    createdAt: now,
    updatedAt: now,
    completedAt: null,
  };
}

/** Today's date as YYYY-MM-DD in local time. */
export function todayKey(date = new Date()) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function isOverdue(task, today = todayKey()) {
  return !task.completed && Boolean(task.dueDate) && task.dueDate < today;
}

export function filterTasks(tasks, { search = '', status = 'all', priority = 'all' }) {
  const query = search.trim().toLowerCase();
  return tasks.filter((task) => {
    if (query && !task.title.toLowerCase().includes(query)) return false;
    if (status === 'active' && task.completed) return false;
    if (status === 'completed' && !task.completed) return false;
    if (priority !== 'all' && task.priority !== priority) return false;
    return true;
  });
}

export function sortTasks(tasks, sortBy = 'newest') {
  const list = [...tasks];
  const byNewest = (a, b) => b.createdAt.localeCompare(a.createdAt);
  switch (sortBy) {
    case 'oldest':
      return list.sort((a, b) => a.createdAt.localeCompare(b.createdAt));
    case 'priority':
      return list.sort(
        (a, b) => PRIORITY_RANK[a.priority] - PRIORITY_RANK[b.priority] || byNewest(a, b)
      );
    case 'due':
      return list.sort((a, b) => {
        if (!a.dueDate && !b.dueDate) return byNewest(a, b);
        if (!a.dueDate) return 1;
        if (!b.dueDate) return -1;
        return a.dueDate.localeCompare(b.dueDate) || byNewest(a, b);
      });
    case 'newest':
    default:
      return list.sort(byNewest);
  }
}

export function getStats(tasks, today = todayKey()) {
  const total = tasks.length;
  const completed = tasks.filter((t) => t.completed).length;
  const active = total - completed;
  const overdue = tasks.filter((t) => isOverdue(t, today)).length;
  const byPriority = PRIORITIES.reduce((acc, p) => {
    const group = tasks.filter((t) => t.priority === p);
    acc[p] = { total: group.length, completed: group.filter((t) => t.completed).length };
    return acc;
  }, {});
  const completionRate = total === 0 ? 0 : Math.round((completed / total) * 100);
  return { total, completed, active, overdue, byPriority, completionRate };
}

export function formatDueDate(dueDate, today = todayKey()) {
  if (!dueDate) return '';
  if (dueDate === today) return 'Today';
  const [y, m, d] = dueDate.split('-').map(Number);
  const date = new Date(y, m - 1, d);
  const t = new Date(today + 'T00:00:00');
  const diffDays = Math.round((date - t) / 86400000);
  if (diffDays === 1) return 'Tomorrow';
  if (diffDays === -1) return 'Yesterday';
  return date.toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== t.getFullYear() ? 'numeric' : undefined,
  });
}

/** Validates data loaded from storage so a corrupt entry never crashes the app. */
export function sanitizeTasks(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter((t) => t && typeof t === 'object' && typeof t.title === 'string' && t.title.trim())
    .map((t) => ({
      id: typeof t.id === 'string' && t.id ? t.id : createId(),
      title: t.title.trim(),
      priority: PRIORITIES.includes(t.priority) ? t.priority : 'medium',
      dueDate: typeof t.dueDate === 'string' ? t.dueDate : '',
      completed: Boolean(t.completed),
      createdAt: typeof t.createdAt === 'string' ? t.createdAt : new Date().toISOString(),
      updatedAt: typeof t.updatedAt === 'string' ? t.updatedAt : new Date().toISOString(),
      completedAt: typeof t.completedAt === 'string' ? t.completedAt : null,
    }));
}
