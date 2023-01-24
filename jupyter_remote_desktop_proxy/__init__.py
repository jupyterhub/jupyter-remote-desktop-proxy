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
    vncserver = which('vncserver')

    if vncserver:
        vnc_args = [
            vncserver,
        ]
        socket_args = []
    else:
        # Use bundled tigervnc
        vnc_args = [
            os.path.join(HERE, 'share/tigervnc/bin/vncserver'),
            '-rfbunixpath',
            sockets_path,
        ]
        socket_args = ['--unix-target', sockets_path]

    vnc_command = ' '.join(
        shlex.quote(p)
        for p in (
            vnc_args
            + [
                '-verbose',
                '-xstartup',
                os.path.join(HERE, 'share/xstartup'),
                '-geometry',
                '1680x1050',
                '-SecurityTypes',
                'None',
                '-fg',
                ':1',
            ]
        )
    )
    return {
        'command': [
            'websockify',
            '-v',
            '--web',
            os.path.join(HERE, 'share/web/noVNC-1.2.0'),
            '--heartbeat',
            '30',
            '5901',
        ]
        + socket_args
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}'],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True,
    }
