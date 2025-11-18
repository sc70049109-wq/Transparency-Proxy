from flask import Flask, redirect
import docker

app = Flask(__name__)
client = docker.from_env()

# Docker configuration
FIREFOX_IMAGE = "jlesage/firefox:latest"
CONTAINER_NAME = "transparency-firefox"
FIXED_PORT = 3001  # Fixed port for Firefox web UI

@app.route("/")
def index():
    """
    Main page. Redirects to the running Firefox container.
    """
    try:
        container = client.containers.get(CONTAINER_NAME)
        if container.status != "running":
            container.start()
    except docker.errors.NotFound:
        # Run the container if it doesn't exist
        client.containers.run(
            FIREFOX_IMAGE,
            name=CONTAINER_NAME,
            detach=True,
            ports={"5800/tcp": FIXED_PORT},
            shm_size="2g",
            restart_policy={"Name": "always"}
        )

    return redirect(f"http://localhost:{FIXED_PORT}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
