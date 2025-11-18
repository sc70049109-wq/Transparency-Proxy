from flask import Flask, send_from_directory, redirect
import subprocess
import docker

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/open")
def open_proxy():
    container_name = "transparency-chrome"
    client = docker.from_env()

    # Check if container exists
    try:
        container = client.containers.get(container_name)
        if container.status != "running":
            container.start()
    except docker.errors.NotFound:
        # Start new container
        subprocess.run([
            "docker", "run", "-d",
            "--name", container_name,
            "-p", "3001:5800",
            "--shm-size=2g",
            "lscr.io/linuxserver/chromium:latest"
        ])

    # Redirect to chromium viewer
    return redirect("http://localhost:3001", code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
