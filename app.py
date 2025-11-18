from flask import Flask, redirect, send_from_directory
import subprocess
import docker
import time

app = Flask(__name__, static_folder='static')

FIREFOX_CONTAINER_NAME = "transparency-firefox"
FIREFOX_IMAGE = "jlesage/firefox:latest"
FIREFOX_PORT = 3001  # change this if you want another port

client = docker.from_env()

def start_firefox_container():
    # Check if container already exists
    try:
        container = client.containers.get(FIREFOX_CONTAINER_NAME)
        if container.status != "running":
            container.start()
            time.sleep(5)  # give container time to start
    except docker.errors.NotFound:
        # Create and start container
        client.containers.run(
            FIREFOX_IMAGE,
            name=FIREFOX_CONTAINER_NAME,
            detach=True,
            ports={'5800/tcp': FIREFOX_PORT},
            shm_size='2g',
            restart_policy={"Name": "always"}
        )
        time.sleep(5)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/open-firefox')
def open_firefox():
    start_firefox_container()
    # Redirect user to the Firefox container VNC web port
    return redirect(f"http://localhost:{FIREFOX_PORT}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
