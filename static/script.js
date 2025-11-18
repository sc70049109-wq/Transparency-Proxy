// Toggle dark/light mode
document.addEventListener("DOMContentLoaded", () => {
  const body = document.body;
  const toggleBtn = document.createElement("button");
  toggleBtn.innerText = "☀️/🌙";
  toggleBtn.classList.add("btn-glass");
  toggleBtn.style.position = "fixed";
  toggleBtn.style.top = "1rem";
  toggleBtn.style.right = "1rem";
  toggleBtn.style.zIndex = "1000";

  toggleBtn.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
  });

  body.appendChild(toggleBtn);
});
