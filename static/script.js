// Optional JS for theme toggle or animations

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".btn-glass");
  btn.addEventListener("click", (e) => {
    // Redirect to Flask root route
    e.preventDefault();
    window.location.href = "/";
  });
});
