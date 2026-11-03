import Icon from './Icon.jsx';

export default function Header({ theme, onToggleTheme }) {
  const today = new Date().toLocaleDateString(undefined, {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';

  return (
    <header className="header">
      <div className="brand">
        <div className="brand-mark" aria-hidden="true">
          <Icon name="check" size={20} strokeWidth={3} />
        </div>
        <div>
          <h1 className="brand-name">Taskflow</h1>
          <p className="brand-sub">
            {greeting} · {today}
          </p>
        </div>
      </div>
      <button
        type="button"
        className="icon-btn theme-toggle"
        onClick={onToggleTheme}
        aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        title={theme === 'dark' ? 'Light mode' : 'Dark mode'}
      >
        <Icon name={theme === 'dark' ? 'sun' : 'moon'} />
      </button>
    </header>
  );
}
