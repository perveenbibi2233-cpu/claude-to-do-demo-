import { describe, it, expect } from 'vitest';
import { render, screen, within, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App.jsx';
import { STORAGE_KEY } from '../hooks/useTasks.js';

const stat = (name) => screen.getByTestId(`stat-${name}`).textContent;
const taskList = () => screen.getByRole('list');

async function addTask(user, title, priority) {
  await user.type(screen.getByLabelText('New task title'), title);
  if (priority) {
    const group = screen.getAllByRole('radiogroup', { name: 'Priority' })[0];
    await user.click(within(group).getByLabelText(priority));
  }
  await user.click(screen.getByRole('button', { name: /add task/i }));
}

describe('App', () => {
  it('shows an empty state initially', () => {
    render(<App />);
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
    expect(stat('total')).toBe('0');
  });

  it('adds a task and rejects an empty title', async () => {
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole('button', { name: /add task/i }));
    expect(screen.getByRole('alert')).toHaveTextContent('Please enter a task title.');

    await addTask(user, 'Write tests', 'High');
    expect(within(taskList()).getByText('Write tests')).toBeInTheDocument();
    expect(within(taskList()).getByText('High')).toBeInTheDocument();
    expect(stat('total')).toBe('1');
    expect(screen.getByLabelText('New task title')).toHaveValue('');
  });

  it('marks a task as completed and updates statistics', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'Task A');
    await addTask(user, 'Task B');
    await user.click(screen.getByRole('checkbox', { name: /mark "Task A" as completed/i }));
    expect(stat('completed')).toBe('1');
    expect(stat('active')).toBe('1');
    expect(screen.getByRole('img', { name: '50% of tasks completed' })).toBeInTheDocument();
  });

  it('edits a task title and priority', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'Old title');
    await user.click(screen.getByRole('button', { name: 'Edit "Old title"' }));
    const input = screen.getByLabelText('Edit task title');
    await user.clear(input);
    await user.type(input, 'New title');
    const group = screen.getAllByRole('radiogroup', { name: 'Priority' })[1];
    await user.click(within(group).getByLabelText('Low'));
    await user.click(screen.getByRole('button', { name: 'Save' }));
    expect(within(taskList()).getByText('New title')).toBeInTheDocument();
    expect(within(taskList()).getByText('Low')).toBeInTheDocument();
    expect(screen.queryByText('Old title')).not.toBeInTheDocument();
  });

  it('cancels editing with Escape', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'Keep me');
    await user.click(screen.getByRole('button', { name: 'Edit "Keep me"' }));
    await user.type(screen.getByLabelText('Edit task title'), ' changed{Escape}');
    expect(within(taskList()).getByText('Keep me')).toBeInTheDocument();
  });

  it('deletes a task and can undo', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'Delete me');
    await user.click(screen.getByRole('button', { name: 'Delete "Delete me"' }));
    await waitFor(() => expect(screen.queryByText('Delete me')).not.toBeInTheDocument());
    expect(stat('total')).toBe('0');
    await user.click(screen.getByRole('button', { name: 'Undo' }));
    expect(within(taskList()).getByText('Delete me')).toBeInTheDocument();
  });

  it('searches and filters tasks', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'Buy groceries', 'Low');
    await addTask(user, 'Finish report', 'High');
    await addTask(user, 'Call mom', 'Medium');

    await user.type(screen.getByLabelText('Search tasks'), 'report');
    expect(within(taskList()).getAllByRole('listitem')).toHaveLength(1);
    await user.click(screen.getByRole('button', { name: 'Clear search' }));

    await user.selectOptions(screen.getByLabelText('Filter by priority'), 'low');
    expect(within(taskList()).getByText('Buy groceries')).toBeInTheDocument();
    expect(within(taskList()).getAllByRole('listitem')).toHaveLength(1);
    await user.selectOptions(screen.getByLabelText('Filter by priority'), 'all');

    await user.click(screen.getByRole('checkbox', { name: /mark "Call mom"/i }));
    await user.click(screen.getByRole('tab', { name: /completed/i }));
    expect(within(taskList()).getAllByRole('listitem')).toHaveLength(1);
    await user.click(screen.getByRole('tab', { name: /active/i }));
    expect(within(taskList()).getAllByRole('listitem')).toHaveLength(2);

    await user.type(screen.getByLabelText('Search tasks'), 'zzz');
    expect(screen.getByText('No matching tasks')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Clear filters' }));
    expect(within(taskList()).getAllByRole('listitem')).toHaveLength(3);
  });

  it('persists tasks to localStorage and restores them', async () => {
    const user = userEvent.setup();
    const { unmount } = render(<App />);
    await addTask(user, 'Persist me', 'High');
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    expect(saved[0]).toMatchObject({ title: 'Persist me', priority: 'high' });
    unmount();
    render(<App />);
    expect(within(taskList()).getByText('Persist me')).toBeInTheDocument();
  });

  it('survives corrupt localStorage data', () => {
    localStorage.setItem(STORAGE_KEY, '{not json');
    render(<App />);
    expect(screen.getByText('No tasks yet')).toBeInTheDocument();
  });

  it('clears completed tasks', async () => {
    const user = userEvent.setup();
    render(<App />);
    await addTask(user, 'One');
    await addTask(user, 'Two');
    await user.click(screen.getByRole('checkbox', { name: /mark "One"/i }));
    await user.click(screen.getByRole('button', { name: 'Clear completed' }));
    expect(screen.queryByText('One')).not.toBeInTheDocument();
    expect(stat('total')).toBe('1');
  });
});
