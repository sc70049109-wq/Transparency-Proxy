from flask import Flask, render_template, redirect, url_for
import docker
import random

app = Flask(__name__)
client = docker.from_env()

# Change this to your Firefox Docker image
FIREFOX_IMAGE = "jlesage/firefox:latest"
START_PORT = 3001

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/open-firefox")
def open_firefox():
    # pick a random port above START_PORT to avoid collisions
    port = random.randint(START_PORT, START_PORT + 1000)
    container_name = f"transparency-firefox-{port}"

    # run the container
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

    # redirect user to the Firefox VNC/web UI
    return redirect(f"http://{request.host.split(':')[0]}:{port}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
