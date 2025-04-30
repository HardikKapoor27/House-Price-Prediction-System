document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('nav-bar');

  // Pages where login should appear
  const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';

  fetch('https://house-price-prediction-system-503i.onrender.com/account', {
    method: 'GET',
    credentials: 'include'
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      nav.innerHTML = `
        <a href="index.html" class="nav-button">Home</a>
        <a href="app.html" class="nav-button">House Price Predictor</a>
        <a href="about.html" class="nav-button">About Us</a>
        <a href="contact.html" class="nav-button">Contact Us</a>
        <a href="account.html" class="nav-button">Account</a>
      `;
    } else {
      // Only show login/register on home
      nav.innerHTML = `
        <a href="index.html" class="nav-button">Home</a>
        <a href="app.html" class="nav-button">House Price Predictor</a>
        <a href="about.html" class="nav-button">About Us</a>
        <a href="contact.html" class="nav-button">Contact Us</a>
        ${isHome ? `<a href="login.html" class="nav-button">Login</a><a href="register.html" class="nav-button">Register</a>` : ''}
      `;
    }
  });
});
