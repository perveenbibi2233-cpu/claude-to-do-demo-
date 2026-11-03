import { useEffect, useState } from 'react';

export function readStorage(key, fallback) {
  try {
    const raw = window.localStorage.getItem(key);
    return raw === null ? fallback : JSON.parse(raw);
  } catch {
    return fallback;
  }
}

export function useLocalStorage(key, initialValue, parse = (v) => v) {
  const [value, setValue] = useState(() => parse(readStorage(key, initialValue)));

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Storage may be full or unavailable (private mode); the app keeps working in memory.
    }
  }, [key, value]);

  return [value, setValue];
}
