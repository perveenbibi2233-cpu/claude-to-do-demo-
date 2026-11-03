import { describe, it, expect } from 'vitest';
import {
  createTask,
  filterTasks,
  sortTasks,
  getStats,
  isOverdue,
  sanitizeTasks,
  formatDueDate,
} from '../utils/tasks.js';

const make = (overrides) => ({ ...createTask({ title: 'x' }), ...overrides });

describe('task utilities', () => {
  it('creates a trimmed task with defaults', () => {
    const t = createTask({ title: '  Buy milk  ' });
    expect(t.title).toBe('Buy milk');
    expect(t.priority).toBe('medium');
    expect(t.completed).toBe(false);
    expect(t.id).toBeTruthy();
  });

  it('falls back to medium for an unknown priority', () => {
    expect(createTask({ title: 'a', priority: 'urgent' }).priority).toBe('medium');
  });

  it('filters by search, status and priority', () => {
    const tasks = [
      make({ title: 'Write report', priority: 'high', completed: false }),
      make({ title: 'Read book', priority: 'low', completed: true }),
      make({ title: 'Report bug', priority: 'low', completed: false }),
    ];
    expect(filterTasks(tasks, { search: 'REPORT' })).toHaveLength(2);
    expect(filterTasks(tasks, { status: 'completed' })).toHaveLength(1);
    expect(filterTasks(tasks, { status: 'active', priority: 'low' })[0].title).toBe('Report bug');
  });

  it('sorts by priority, then due date with undated tasks last', () => {
    const tasks = [
      make({ title: 'low', priority: 'low', dueDate: '2026-01-01', createdAt: '1' }),
      make({ title: 'high', priority: 'high', dueDate: '', createdAt: '2' }),
      make({ title: 'med', priority: 'medium', dueDate: '2025-06-01', createdAt: '3' }),
    ];
    expect(sortTasks(tasks, 'priority').map((t) => t.title)).toEqual(['high', 'med', 'low']);
    expect(sortTasks(tasks, 'due').map((t) => t.title)).toEqual(['med', 'low', 'high']);
    expect(sortTasks(tasks, 'newest').map((t) => t.title)).toEqual(['med', 'high', 'low']);
  });

  it('computes statistics', () => {
    const tasks = [
      make({ priority: 'high', completed: true }),
      make({ priority: 'high', completed: false, dueDate: '2020-01-01' }),
      make({ priority: 'low', completed: false }),
      make({ priority: 'low', completed: true, dueDate: '2020-01-01' }),
    ];
    const s = getStats(tasks, '2026-11-03');
    expect(s).toMatchObject({ total: 4, completed: 2, active: 2, overdue: 1, completionRate: 50 });
    expect(s.byPriority.high).toEqual({ total: 2, completed: 1 });
    expect(s.byPriority.medium).toEqual({ total: 0, completed: 0 });
  });

  it('detects overdue tasks only when active and past due', () => {
    expect(isOverdue(make({ dueDate: '2026-11-02' }), '2026-11-03')).toBe(true);
    expect(isOverdue(make({ dueDate: '2026-11-03' }), '2026-11-03')).toBe(false);
    expect(isOverdue(make({ dueDate: '2026-11-02', completed: true }), '2026-11-03')).toBe(false);
  });

  it('formats relative due dates', () => {
    expect(formatDueDate('2026-11-03', '2026-11-03')).toBe('Today');
    expect(formatDueDate('2026-11-04', '2026-11-03')).toBe('Tomorrow');
    expect(formatDueDate('2026-11-02', '2026-11-03')).toBe('Yesterday');
  });

  it('sanitizes corrupt storage data', () => {
    expect(sanitizeTasks(null)).toEqual([]);
    expect(sanitizeTasks('nope')).toEqual([]);
    const cleaned = sanitizeTasks([{ title: 'ok', priority: 'bogus' }, { title: '' }, 5, null]);
    expect(cleaned).toHaveLength(1);
    expect(cleaned[0].priority).toBe('medium');
  });
});
