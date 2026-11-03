import { useEffect } from 'react';
import { useLocalStorage } from './useLocalStorage.js';

function systemTheme() {
  return typeof window !== 'undefined' &&
    window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}

export function useTheme() {
  const [theme, setTheme] = useLocalStorage('taskflow.theme', systemTheme(), (v) =>
    v === 'dark' || v === 'light' ? v : systemTheme()
  );

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  const toggleTheme = () => setTheme((t) => (t === 'dark' ? 'light' : 'dark'));
  return { theme, toggleTheme };
}
