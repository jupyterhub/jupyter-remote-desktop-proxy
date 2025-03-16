import os
import shlex
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_websockify():
    vncserver = which('vncserver')
    if not vncserver:
        raise RuntimeError(
            "vncserver executable not found, please install a VNC server"
        )

    # {unix_socket} is expanded by jupyter-server-proxy
    vnc_args = [vncserver, '-rfbunixpath', '{unix_socket}']

    xstartup = os.getenv("JUPYTER_REMOTE_DESKTOP_PROXY_XSTARTUP")
    if not xstartup and not os.path.exists(os.path.expanduser('~/.vnc/xstartup')):
        xstartup = os.path.join(HERE, 'share/xstartup')
    if xstartup:
        vnc_args.extend(['-xstartup', xstartup])

    vnc_command = shlex.join(
        vnc_args
        + [
            '-verbose',
            '-fg',
            '-geometry',
            '1680x1050',
            '-SecurityTypes',
            'None',
        ]
    )

    return {
        'command': ['/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'timeout': 30,
        'new_browser_window': True,
        # We want the launcher entry to point to /desktop/, not to /desktop-websockify/
        # /desktop/ is the user facing URL, while /desktop-websockify/ now *only* serves
        # websockets.
        "launcher_entry": {"title": "Desktop", "path_info": "desktop"},
        "unix_socket": True,
        "raw_socket_proxy": True,
    }
