// Neon glow / mouse tracking (optional effect)
document.addEventListener("mousemove", (e) => {
    document.documentElement.style.setProperty("--mx", e.clientX + "px");
    document.documentElement.style.setProperty("--my", e.clientY + "px");
});

// Enter button → open new tab and call backend
const btn = document.getElementById("enter-btn");

btn.addEventListener("click", async () => {
    const newTab = window.open("about:blank", "_blank");
    if (!newTab) return alert("Popup blocked!");

    try {
        const resp = await fetch("/start", { method: "POST" });
        const data = await resp.json();
        if (data.status === "ok") {
            newTab.location.href = data.url;
        } else {
            newTab.document.write(`<h2>Error</h2><pre>${data.error}</pre>`);
        }
    } catch (err) {
        newTab.document.write(`<h2>Network Error</h2><pre>${err}</pre>`);
    }
});

// Theme toggle
const toggle = document.getElementById("theme-toggle");
if (toggle) {
    toggle.addEventListener("click", () => {
        const b = document.body;
        b.classList.toggle("dark");
        b.classList.toggle("light");
        toggle.textContent = b.classList.contains("dark") ? "🌙" : "☀️";
    });
}
