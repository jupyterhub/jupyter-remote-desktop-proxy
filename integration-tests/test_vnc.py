"""
Test the VNC server is serving images
"""

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
        "-p",
        "8888:8888",
        "--rm",
        "-d",
        "--security-opt",
        "seccomp=unconfined",
        "--security-opt",
        "apparmor=unconfined",
        container_image,
        "jupyter",
        "server",
        f"--IdentityProvider.token={token}",
    ]
    container_name = subprocess.check_output(cmd).decode()
    # FIXME: Instead, wait for container to be ready here
    time.sleep(5)

    try:
        # FIXME: Dynamically allocate this port
        yield (8888, token)
    finally:
        subprocess.check_call(['docker', 'stop', container_name])


def test_vnc_screenshot(container, image_diff):
    port, token = container
    websocat_proc = subprocess.Popen(
        [
            'websocat',
            '--binary',
            '--exit-on-eof',
            # FIXME: Dynamically allocate this port too
            'tcp-l:127.0.0.1:5999',
            f'ws://127.0.0.1:{port}/desktop-websockify/?token={token}',
        ]
    )
    try:
        with api.connect('127.0.0.1::5999') as client:
            time.sleep(5)
            client.captureScreen("test.jpeg")
            assert image_diff(
                str(REPO_ROOT / "integration-tests/expected.jpeg"), "test.jpeg"
            )
        # subprocess.check_call([
        #     'vncdo',
        #     '-vv',
        #     '-s',
        #     '127.0.0.1::5999',
        #     'expect',
        #     '5'
        # ])
        # time.sleep(10)
        # subprocess.check_call([
        #     'vncdo',
        #     '-s',
        #     '127.0.0.1::5999',
        #     'capture',
        #     'capture.jpeg'
        # ])
    finally:
        # Explicitly shutdown vncdo, as otherwise a stray thread keeps
        # running forever
        api.shutdown()

        websocat_proc.kill()
        websocat_proc.wait()
