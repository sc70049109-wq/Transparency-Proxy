from flask import Flask, send_from_directory, redirect, request
import docker
import random
import os

app = Flask(__name__, static_folder="static")
client = docker.from_env()

FIREFOX_IMAGE = "jlesage/firefox:latest"
START_PORT = 3001

# Serve index.html at root
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Serve proxy.html if needed
@app.route("/proxy")
def proxy():
    return send_from_directory(app.static_folder, "proxy.html")

# Open Firefox Docker container
@app.route("/open-firefox")
def open_firefox():
    port = random.randint(START_PORT, START_PORT + 1000)
    container_name = f"transparency-firefox-{port}"

    try:
        container = client.containers.run(
            FIREFOX_IMAGE,
            name=container_name,
            ports={"5800/tcp": port},
            detach=True,
            shm_size="2g",
            remove=True
        )
    except docker.errors.APIError as e:
        return f"Error starting Firefox container: {e.explanation}"

    host = request.host.split(":")[0]
    return redirect(f"http://{host}:{port}")

# Serve static files (CSS, JS, icons)
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
