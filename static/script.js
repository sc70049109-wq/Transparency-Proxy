document.addEventListener("DOMContentLoaded", () => {
  const enterButton = document.getElementById("enterBtn");
  const themeToggle = document.getElementById("themeToggle");

  enterButton.addEventListener("click", async () => {
    const spinner = window.open("proxy.html", "_blank");
    try {
      const response = await fetch("/start", { method: "POST" });
      const data = await response.json();
      if (data.status === "ok" && data.url) {
        spinner.location.href = data.url;
      } else {
        spinner.close();
        alert("Failed: " + data.error);
      }
    } catch (err) {
      spinner.close();
      console.error(err);
      alert("Error connecting to server.");
    }
  });

  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light-mode");
    document.body.classList.toggle("dark-mode");
  });
});
