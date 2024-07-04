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

    # TurboVNC and TigerVNC share the same origin and both use a Perl script
    # as the executable vncserver. We can determine if vncserver is TigerVNC
    # by searching tigervnc string in the Perl script.
    #
    # The content of the vncserver executable can differ depending on how
    # TigerVNC and TurboVNC has been distributed. Below are files known to be
    # read in some situations:
    #
    # - https://github.com/TigerVNC/tigervnc/blob/v1.13.1/unix/vncserver/vncserver.in
    # - https://github.com/TurboVNC/turbovnc/blob/3.1.1/unix/vncserver.in
    #
    with open(vncserver) as vncserver_file:
        is_tigervnc = "tigervnc" in vncserver_file.read().casefold()

    if is_tigervnc:
        unix_socket = True
        vnc_args = [vncserver, '-rfbunixpath', "{unix_socket}"]
    else:
        unix_socket = False
        vnc_args = [vncserver, '-localhost', '-rfbport', '{port}']

    if not os.path.exists(os.path.expanduser('~/.vnc/xstartup')):
        vnc_args.extend(['-xstartup', os.path.join(HERE, 'share/xstartup')])

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
        "unix_socket": unix_socket,
        "raw_socket_proxy": True,
    }
