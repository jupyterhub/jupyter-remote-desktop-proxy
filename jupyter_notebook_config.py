c.ServerProxy.servers = {
    'lxde': {
        'command': [
            # '/usr/local/bin/websockify',
            '/opt/conda/bin/websockify',
            '-v',
            '--web', '/usr/share/novnc',
            '5901',
            '--',
            'vncserver',
            '-verbose',
            '-xstartup', 'startlxde',
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
