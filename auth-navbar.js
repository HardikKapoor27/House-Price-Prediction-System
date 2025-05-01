document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('nav-right');
  const currentPage = window.location.pathname;
  const showAuthButtons = currentPage.endsWith('index.html') || currentPage.endsWith('/') || currentPage.endsWith('auth.html');

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
    nav.innerHTML = `
      <a href="index.html" class="nav-button">Home</a>
      <a href="app.html" class="nav-button">House Price Predictor</a>
      <a href="about.html" class="nav-button">About Us</a>
      <a href="contact.html" class="nav-button">Contact Us</a>
      ${showAuthButtons ? `<a href="auth.html" class="nav-button">Login/Register</a>` : ''}
    `;
  });
});
