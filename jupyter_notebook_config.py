import os

if os.getenv('DESKTOP_PACKAGE') == 'lxde':
    xstartup = 'startlxde'
elif os.getenv('DESKTOP_PACKAGE') == 'xfce4':
    xstartup = 'xfce4-session'
else:
    xstartup = 'xterm'

vnc_socket = os.path.join(os.getenv('HOME'), '.vnc', 'socket')
c.ServerProxy.servers = {
    'Desktop': {
        'command': [
            '/opt/conda/bin/websockify',
            '-v',
            '--web', '/opt/noVNC-1.1.0',
            '--heartbeat', '30',
            '5901',
            '--unix-target', vnc_socket,
            '--',
            'vncserver',
            '-verbose',
            '-xstartup', xstartup,
            '-geometry', '1024x768',
            '-SecurityTypes', 'None',
            '-rfbunixpath', vnc_socket,
            '-fg',
            ':1',
        ],
        'absolute_url': False,
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
    }
}
