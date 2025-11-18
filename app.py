from flask import Flask, render_template, redirect
import subprocess

app = Flask(__name__)

CHROMIUM_CONTAINER = "transparency-chrome"
CHROMIUM_PORT = 3001
CHROMIUM_IMAGE = "lscr.io/linuxserver/chromium:latest"

def container_running(name):
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={name}"], capture_output=True, text=True
    )
    return bool(result.stdout.strip())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/open")
def open_proxy():
    if not container_running(CHROMIUM_CONTAINER):
        subprocess.run([
            "docker", "run", "-d",
            "--name", CHROMIUM_CONTAINER,
            "-p", f"{CHROMIUM_PORT}:5800",
            "-e", "PUID=1000",
            "-e", "PGID=1000",
            "-e", "TZ=America/New_York",
            "--shm-size=2g",
            CHROMIUM_IMAGE
        ])
    return redirect(f"http://localhost:{CHROMIUM_PORT}/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
