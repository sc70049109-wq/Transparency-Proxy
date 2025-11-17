// script.js

document.addEventListener("DOMContentLoaded", () => {
  const enterButton = document.getElementById("enterBtn");
  const themeToggle = document.getElementById("themeToggle");

  // Enter Transparency Proxy button click
  enterButton.addEventListener("click", async () => {
    try {
      const response = await fetch("/start", { method: "POST" });
      const data = await response.json();

      if (data.status === "ok" && data.url) {
        window.open(data.url, "_blank");
      } else {
        alert("Failed to start Chromium container: " + data.error);
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to server.");
    }
  });

  // Theme toggle: dark/light mode
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    document.body.classList.toggle("dark-mode");
  });
});
