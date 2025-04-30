document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('nav-right');

  // Pages where login should appear
  const isHome = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';

  fetch('https://house-price-prediction-system-503i.onrender.com/account', {
  method: 'GET',
  credentials: 'include'
 })
.then(res => {
  if (!res.ok) throw new Error('Unauthorized');
  return res.json();
 })
.then(data => {
  if (data.status === 'success') {
    nav.innerHTML = `
      <a href="index.html" class="nav-button">Home</a>
      <a href="app.html" class="nav-button">House Price Predictor</a>
      <a href="about.html" class="nav-button">About Us</a>
      <a href="contact.html" class="nav-button">Contact Us</a>
      <a href="account.html" class="nav-button">Account</a>
    `;
  }
})
.catch(() => {
  // Even if fetch fails (401), render login/register links
  nav.innerHTML = `
    <a href="index.html" class="nav-button">Home</a>
    <a href="app.html" class="nav-button">House Price Predictor</a>
    <a href="about.html" class="nav-button">About Us</a>
    <a href="contact.html" class="nav-button">Contact Us</a>
    ${isHome ? `<a href="login.html" class="nav-button">Login</a><a href="register.html" class="nav-button">Register</a>` : ''}
  `;
});

});
