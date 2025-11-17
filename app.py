#!/usr/bin/env python3
from flask import Flask, jsonify, request
import docker
import random
import socket

app = Flask(__name__)
client = docker.from_env()

CHROME_IMAGE = "overclockedllama/docker-chromium"  # Soneji-based image

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port

@app.route("/start", methods=["POST"])
def start():
    host_port = find_free_port()
    container_name = f"transparency-chromium-{host_port}"
    try:
        container = client.containers.run(
            CHROME_IMAGE,
            detach=True,
            name=container_name,
            ports={"5800/tcp": host_port},
            shm_size="2g",
        )
    except docker.errors.APIError as e:
        return jsonify(status="error", error=str(e)), 500

    # Build the URL for the VNC / web interface
    host = request.host.split(":")[0]
    if host in ("", "0.0.0.0"):
        host = "localhost"
    url = f"http://{host}:{host_port}/"
    return jsonify(status="ok", url=url, container=container_name)

@app.route("/stop", methods=["POST"])
def stop():
    data = request.get_json() or {}
    cname = data.get("container")
    if not cname:
        return jsonify(status="error", error="container name required"), 400
    try:
        cont = client.containers.get(cname)
        cont.stop()
        cont.remove()
    except docker.errors.NotFound:
        return jsonify(status="error", error="container not found"), 404
    except docker.errors.APIError as e:
        return jsonify(status="error", error=str(e)), 500

    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
