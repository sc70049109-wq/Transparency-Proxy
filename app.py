from flask import Flask, redirect, send_from_directory
import subprocess

app = Flask(__name__, static_folder="static")

CHROME_PORT = 3001
DOCKER_NAME = "transparency-chrome"
DOCKER_IMAGE = "lscr.io/linuxserver/chromium:latest"

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/open")
def open_proxy():
    # Check if container is running
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", DOCKER_NAME],
            capture_output=True, text=True, check=True
        )
        running = result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        running = False

    # Start container if not running
    if not running:
        subprocess.run([
            "docker", "run", "-d",
            "--name", DOCKER_NAME,
            "-p", f"{CHROME_PORT}:5800",
            "--shm-size=2g",
            DOCKER_IMAGE
        ], check=True)

    # Redirect to running Chromium
    return redirect(f"http://localhost:{CHROME_PORT}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
