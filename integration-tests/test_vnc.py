"""
Test the VNC server is serving images
"""

import json
import secrets
import subprocess
import tempfile
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
    container_name = f"remote-desktop-proxy-integration-test-{secrets.token_hex(4)}"
    cmd = [
        "docker",
        "run",
        "--publish-all",
        "--rm",
        "--name",
        container_name,
        "--security-opt",
        "seccomp=unconfined",
        "--security-opt",
        "apparmor=unconfined",
        container_image,
        "jupyter",
        "server",
        f"--IdentityProvider.token={token}",
    ]
    proc = subprocess.Popen(cmd)

    print("Waiting for container to come online...")
    # Try 5 times, with a 2s wait in between
    for current_try in range(5):
        time.sleep(5)
        try:
            container_info = json.loads(
                subprocess.check_output(
                    ['docker', 'container', 'inspect', container_name]
                ).decode()
            )
        except subprocess.CalledProcessError as e:
            print(f"Container not ready yet, inspect returned {e.returncode}")
            time.sleep(2)
            continue

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
        proc.kill()
        proc.wait()
        subprocess.check_call(['docker', 'container', 'stop', container_name])


def test_vnc_screenshot(container, image_diff, unused_tcp_port):
    origin, token = container
    websocat_proc = subprocess.Popen(
        [
            'websocat',
            '--binary',
            '--exit-on-eof',
            f'tcp-l:127.0.0.1:{unused_tcp_port}',
            f'ws://{origin}/desktop-websockify/?token={token}',
        ]
    )
    print(f"websocat proxying 127.0.0.1:{unused_tcp_port} to VNC server")
    try:
        # :: is used to indicate port, as that is what VNC expects.
        # A single : is used to indicate display number. In our case, we
        # do not use multiple displays so no need to specify that.
        with api.connect(
            f'127.0.0.1::{unused_tcp_port}'
        ) as client, tempfile.TemporaryDirectory() as d:
            # Wait a bit for the desktop to fully render, as it is only started
            # up when our connect call completes.
            # FIXME: Repeatedly take a few screenshots here in a retry loop until
            # a timeout or the images match
            time.sleep(15)
            screenshot_target = Path(d) / "screenshot.jpeg"
            print("Connected to VNC server. Attempting to capture screenshot...")
            client.captureScreen(str(screenshot_target))

            # This asserts if the images are different, so test will fail
            image_diff(REPO_ROOT / "integration-tests/expected.jpeg", screenshot_target)
    finally:
        # Explicitly shutdown vncdo, as otherwise a stray thread keeps
        # running forever
        api.shutdown()

        websocat_proc.kill()
        websocat_proc.wait()
