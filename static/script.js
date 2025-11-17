// Dark / Light mode toggle
const themeBtn = document.getElementById("theme-btn");
themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("light");
  document.body.classList.toggle("dark");
});

// Open Transparency Proxy button
const enterBtn = document.getElementById("enter-btn");
enterBtn.addEventListener("click", () => {
  // Open proxy.html in a new tab
  window.open("proxy.html", "_blank");

  // Redirect to Flask backend route that launches Chromium
  window.location.href = "/open";
});
