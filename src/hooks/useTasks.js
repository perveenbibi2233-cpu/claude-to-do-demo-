import { useCallback } from 'react';
import { useLocalStorage } from './useLocalStorage.js';
import { createTask, sanitizeTasks, PRIORITIES } from '../utils/tasks.js';

export const STORAGE_KEY = 'taskflow.tasks.v1';

export function useTasks() {
  const [tasks, setTasks] = useLocalStorage(STORAGE_KEY, [], sanitizeTasks);

  const addTask = useCallback(
    (data) => {
      if (!data.title || !data.title.trim()) return null;
      const task = createTask(data);
      setTasks((prev) => [task, ...prev]);
      return task;
    },
    [setTasks]
  );

  const updateTask = useCallback(
    (id, changes) => {
      setTasks((prev) =>
        prev.map((t) => {
          if (t.id !== id) return t;
          const next = { ...t, ...changes, updatedAt: new Date().toISOString() };
          if (typeof next.title === 'string') next.title = next.title.trim();
          if (!next.title) return t;
          if (!PRIORITIES.includes(next.priority)) next.priority = t.priority;
          return next;
        })
      );
    },
    [setTasks]
  );

  const toggleTask = useCallback(
    (id) => {
      setTasks((prev) =>
        prev.map((t) =>
          t.id === id
            ? {
                ...t,
                completed: !t.completed,
                completedAt: t.completed ? null : new Date().toISOString(),
                updatedAt: new Date().toISOString(),
              }
            : t
        )
      );
    },
    [setTasks]
  );

  const deleteTask = useCallback(
    (id) => setTasks((prev) => prev.filter((t) => t.id !== id)),
    [setTasks]
  );

  const restoreTask = useCallback(
    (task, index) =>
      setTasks((prev) => {
        if (prev.some((t) => t.id === task.id)) return prev;
        const next = [...prev];
        next.splice(Math.min(index, next.length), 0, task);
        return next;
      }),
    [setTasks]
  );

  const clearCompleted = useCallback(
    () => setTasks((prev) => prev.filter((t) => !t.completed)),
    [setTasks]
  );

  return { tasks, addTask, updateTask, toggleTask, deleteTask, restoreTask, clearCompleted };
}
