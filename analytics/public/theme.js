// Runs before first paint so the chosen edition (Paper or Carbon) never flashes.
try {
  const edition = localStorage.getItem('circulation-theme');
  if (edition === 'light' || edition === 'dark') document.documentElement.dataset.theme = edition;
} catch (e) { /* storage blocked: follow the system setting */ }
