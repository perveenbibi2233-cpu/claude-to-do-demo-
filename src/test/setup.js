import '@testing-library/jest-dom/vitest';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
  window.localStorage.clear();
});

if (!window.matchMedia) {
  window.matchMedia = () => ({
    matches: false,
    addEventListener() {},
    removeEventListener() {},
  });
}
