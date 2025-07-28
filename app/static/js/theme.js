// Save theme to localStorage
document.getElementById('toggle-theme').addEventListener('click', function () {
  const body = document.body;
  const icon = document.getElementById('theme-icon');
  const currentTheme = body.getAttribute('data-bs-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  body.setAttribute('data-bs-theme', newTheme);
  localStorage.setItem('theme', newTheme);

  // Toggle icon
  icon.classList.toggle('bi-moon', newTheme === 'light');
  icon.classList.toggle('bi-sun', newTheme === 'dark');
});

// Load theme on page load
window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  const icon = document.getElementById('theme-icon');

  document.body.setAttribute('data-bs-theme', savedTheme);
  icon.classList.add(savedTheme === 'light' ? 'bi-moon' : 'bi-sun');
});