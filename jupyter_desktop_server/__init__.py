import os
import shlex
import tempfile
from notebook.utils import url_path_join as ujoin
from tornado.web import StaticFileHandler
from .handlers import DesktopHandler


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_vnc():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    vnc_command = [
        os.path.join(HERE, 'share/tigervnc/bin/vncserver'),
        '-verbose',
        '-xstartup', os.path.join(HERE, 'share/xstartup'),
        '-geometry', '1680x1050',
        '-SecurityTypes', 'None',
        '-rfbunixpath', sockets_path,
        '-fg',
        ':1',
    ]
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.1.0'),
            '--heartbeat', '30',
            '5901',
            '--unix-target', sockets_path,
            '--',
        ] + vnc_command,
        'port': 5901,
        'timeout': 30,
    }


def load_jupyter_server_extension(nbapp):
    # Set up handlers picked up via config
    base_url = nbapp.web_app.settings['base_url']

    web_path = os.path.join(HERE, 'share/web')
    nbapp.web_app.add_handlers('.*', [
        (ujoin(base_url, 'desktop-server/static/(.*)'), StaticFileHandler, {'path': web_path}),
        (ujoin(base_url, 'desktop'), DesktopHandler)
    ])
