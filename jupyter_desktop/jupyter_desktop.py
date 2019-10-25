import os


def setup_desktop():
    VNC_APPLICATION_DIR = os.path.join(os.getenv('CONDA_DIR'), 'vnc')
    return {
        'command': [
            'websockify', '-v',
            '--web', VNC_APPLICATION_DIR + '/noVNC-1.1.0',
            '--heartbeat', '30',
            '5901',
            '--unix-target', VNC_APPLICATION_DIR + '/socket',
            '--',
            VNC_APPLICATION_DIR + '/bin/vncserver',
            '-verbose',
            '-xstartup', VNC_APPLICATION_DIR + '/xstartup',
            '-geometry', '1024x768',
            '-SecurityTypes', 'None',
            '-rfbunixpath', VNC_APPLICATION_DIR + '/socket',
            '-fg',
            ':1',
        ],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
    }
