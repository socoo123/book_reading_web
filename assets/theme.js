(() => {
  const key = 'reading-notes-theme';
  const choices = ['system', 'light', 'dark'];
  let preference = 'system';

  try {
    const saved = localStorage.getItem(key);
    if (choices.includes(saved)) preference = saved;
  } catch {
    // Storage may be unavailable; the theme still works for this page.
  }

  document.documentElement.dataset.theme = preference;

  document.addEventListener('DOMContentLoaded', () => {
    const control = document.querySelector('.theme-control');
    if (!control) return;
    const buttons = [...control.querySelectorAll('button[data-theme-value]')];
    const sync = () => {
      for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.themeValue === preference));
    };

    for (const button of buttons) {
      button.addEventListener('click', () => {
        preference = button.dataset.themeValue;
        document.documentElement.dataset.theme = preference;
        sync();
        try {
          localStorage.setItem(key, preference);
        } catch {
          // Keep the selected appearance even when it cannot be saved.
        }
      });
    }
    sync();
    control.hidden = false;
  });
})();
