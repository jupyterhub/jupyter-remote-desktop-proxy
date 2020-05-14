import os
import shlex
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    vnc_command = ' '.join((shlex.quote(p) for p in [
        os.path.join(HERE, 'share/tigervnc/bin/vncserver'),
        '-verbose',
        '-xstartup', os.path.join(HERE, 'share/xstartup'),
        '-geometry', '1680x1050',
        '-SecurityTypes', 'None',
        '-rfbunixpath', sockets_path,
        '-fg',
        ':1',
    ]))
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.1.0'),
            '--heartbeat', '30',
            '5901',
            '--unix-target', sockets_path,
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}'
        ],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True
    }
