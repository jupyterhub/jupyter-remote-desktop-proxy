import os

if os.getenv('DESKTOP_PACKAGE') == 'lxde':
    xstartup = 'startlxde'
elif os.getenv('DESKTOP_PACKAGE') == 'xfce4':
    xstartup = 'xfce4-session'
else:
    xstartup = 'xterm'

c.ServerProxy.servers = {
    'desktop': {
        'command': [
            # '/usr/local/bin/websockify',
            '/opt/conda/bin/websockify',
            '-v',
            '--web', '/usr/share/novnc',
            '5901',
            '--',
            'vncserver',
            '-verbose',
            '-xstartup', xstartup,
            '-geometry', '1024x768',
            '-SecurityTypes', 'None',
            '-fg',
            ':1',
        ],
        'absolute_url': False,
        'port': 5901,
        'timeout': 30,
        'indexpage': 'vnc.html?autoconnect=true',
    }
}
