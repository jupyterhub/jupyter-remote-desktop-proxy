"""
Test the VNC server is serving images
"""

import json
import secrets
import subprocess
import time
from pathlib import Path

import pytest
from vncdotool import api

REPO_ROOT = Path(__file__).parent.parent


# Rebuild once every test session if needed, relying on docker cache
# to keep that fast
@pytest.fixture(scope="session")
def container_image() -> str:
    """
    Provide a built container image name
    """
    # Use a different tag name here each time, relying on docker cache to
    # keep things fast and never having to deal with stale image problems
    image_name = f"jupyter-remote-desktop-proxy-integration-test:{secrets.token_hex(8)}"
    cmd = ["docker", "build", "-t", image_name, str(REPO_ROOT)]
    subprocess.check_call(cmd)
    return image_name


@pytest.fixture
def container(container_image) -> tuple[str, str]:
    """
    Provide a running container with jupyter server running

    Returns a tuple of (port, token), where port is the *local* port
    that is forwarded to the jupyter server port inside the docker container,
    and token is the authentication token to be used when talking to the
    remote container.
    """
    token = secrets.token_hex(16)
    cmd = [
        "docker",
        "run",
        "--publish-all",
        "--rm",
        "--detach",
        "--security-opt",
        "seccomp=unconfined",
        "--security-opt",
        "apparmor=unconfined",
        container_image,
        "jupyter",
        "server",
        f"--IdentityProvider.token={token}",
    ]
    container_name = subprocess.check_output(cmd).decode().strip()

    print("Waiting for container to come online...")
    # Try 5 times, with a 2s wait in between
    for current_try in range(5):
        container_info = json.loads(
            subprocess.check_output(
                ['docker', 'container', 'inspect', container_name]
            ).decode()
        )

        container_health = container_info[0]["State"]["Health"]["Status"]
        if container_health == "healthy":
            break

        print(f"Current container health status: {container_health}")
        time.sleep(2)
    else:
        raise TimeoutError("Could not start docker container in time")

    exposed_port = container_info[0]["NetworkSettings"]["Ports"]["8888/tcp"][0]
    origin = f"{exposed_port['HostIp']}:{exposed_port['HostPort']}"

    print(f"Container started at {origin}")
    try:
        yield (origin, token)
    finally:
        subprocess.check_call(['docker', 'container', 'stop', container_name])


def test_vnc_screenshot(container, image_diff):
    origin, token = container
    websocat_proc = subprocess.Popen(
        [
            'websocat',
            '--binary',
            '--exit-on-eof',
            # FIXME: Dynamically allocate this port too
            'tcp-l:127.0.0.1:5999',
            f'ws://{origin}/desktop-websockify/?token={token}',
        ]
    )
    try:
        # :: is used to indicate port, as that is what VNC expects.
        # A single : is used to indicate display number. In our case, we
        # do not use multiple displays so no need to specify that.
        with api.connect('127.0.0.1::5999') as client:
            # Wait a couple of seconds for the desktop to fully render
            time.sleep(5)
            client.captureScreen("test.jpeg")

        # This asserts if the images are different, so test will fail
        image_diff(str(REPO_ROOT / "integration-tests/expected.jpeg"), "test.jpeg")
    finally:
        # Explicitly shutdown vncdo, as otherwise a stray thread keeps
        # running forever
        api.shutdown()

        websocat_proc.kill()
        websocat_proc.wait()
