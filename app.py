from flask import Flask, redirect, send_from_directory
import docker
import time

app = Flask(__name__, static_folder='static', static_url_path='')

FIREFOX_CONTAINER_NAME = "transparency-firefox"
FIREFOX_IMAGE = "jlesage/firefox:latest"
FIREFOX_PORT = 3001  # VNC Web port

client = docker.from_env()

def start_firefox_container():
    try:
        container = client.containers.get(FIREFOX_CONTAINER_NAME)
        if container.status != "running":
            container.start()
            time.sleep(5)
    except docker.errors.NotFound:
        client.containers.run(
            FIREFOX_IMAGE,
            name=FIREFOX_CONTAINER_NAME,
            detach=True,
            ports={'5800/tcp': FIREFOX_PORT},
            shm_size='2g',
            restart_policy={"Name": "always"}
        )
        time.sleep(5)

# Serve index.html at root
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Open Firefox container
@app.route('/open-firefox')
def open_firefox():
    start_firefox_container()
    return redirect(f"http://localhost:{FIREFOX_PORT}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
