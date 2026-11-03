# Taskflow — React To-Do App

A modern, responsive to-do app built with **React 18** and **Vite**.

## Features

- **Add, edit and delete tasks.** Edit inline with the pencil button or by double-clicking a task. Enter saves and Escape cancels. A deleted task can be restored with **Undo**.
- **Mark tasks as completed** with an animated checkbox.
- **Priorities:** High, Medium and Low, shown as color-coded badges and accents.
- **Optional due dates**, shown as Today, Tomorrow or Overdue.
- **Search and filters:** instant text search, status tabs (All / Active / Completed), a priority filter, and sorting by newest, oldest, priority or due date.
- **Dashboard:** a completion ring, a progress bar for each priority, and counts for total, active, completed and overdue tasks.
- **Persistence:** tasks and the light/dark theme are saved in `localStorage`. Corrupt stored data is ignored safely instead of crashing the app.
- **Responsive:** works on mobile and desktop, with a light/dark theme toggle.
- **Smooth animations** for entry, exit, the checkbox and progress. Animations are reduced when the user has `prefers-reduced-motion` set.

## Getting started

```bash
npm install
npm run dev       # start the dev server at http://localhost:5173
npm test          # run the test suite (Vitest + Testing Library)
npm run build     # production build in dist/
npm run preview   # serve the production build
```

## Project structure

```
src/
  App.jsx                 # page layout and state wiring
  components/             # Header, StatsDashboard, TaskForm, Toolbar, TaskItem, ...
  hooks/                  # useTasks (CRUD + storage), useLocalStorage, useTheme
  utils/tasks.js          # pure helpers: filter, sort, stats, dates, validation
  styles.css              # design tokens, light/dark themes, animations
  test/                   # unit and component tests
```
