import os
import shlex
import tempfile
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    # Try to find a local install of vncserver script.
    # If installed with jupyter-remote-desktop-proxy.install,
    # it will by default in of two location based on the tigervnc version:
    #   - bundled_bin: tigervnc < 1.11.0
    #   - bundled_exec: tigervnc > 1.11.0
    # If no vncserver is found in the default bundled path, which will
    # look in the user's PATH. If which return None, vncserver was not found
    # and an exception is raised.
    bundled_bin = os.path.join(HERE, 'share/tigervnc/bin')
    bundled_libexec = os.path.join(HERE, 'share/tigervnc/libexec')
    vncserver = which(
        cmd='vncserver',
        path=f"{bundled_bin}:{bundled_libexec}:{os.environ.get('PATH', os.defpath)}"
    )

    if vncserver is None:
        raise FileNotFoundError('jupyter-remote-desktop-proxy: could not find vncserver')

    # TigerVNC provides the option to connect a Unix socket. TurboVNC does not.
    # TurboVNC and TigerVNC share the same origin and both use a Perl script
    # as the executable vncserver. We can determine if vncserver is TigerVNC
    # by searching TigerVNC string in the Perl script.
    with open(vncserver) as vncserver_file:
        is_tigervnc = "TigerVNC" in vncserver_file.read()

    if is_tigervnc:
        vnc_args = [vncserver, '-rfbunixpath', sockets_path]
        socket_args = ['--unix-target', sockets_path]
    else:
        vnc_args = [vncserver]
        socket_args = []

    if not os.path.exists(os.path.expanduser('~/.vnc/xstartup')):
        vnc_args.extend(['-xstartup', os.path.join(HERE, 'share/xstartup')])

    vnc_command = shlex.join(
        vnc_args
        + [
            '-verbose',
            '-geometry',
            '1680x1050',
            '-SecurityTypes',
            'None',
            '-fg',
        ]
    )

    return {
        'command': [
            'websockify',
            '-v',
            '--web',
            os.path.join(HERE, 'share/web/noVNC-1.2.0'),
            '--heartbeat',
            '30',
            '{port}',
        ]
        + socket_args
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True,
    }
