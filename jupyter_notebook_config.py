c.ServerProxy.servers = {
    'lxde': {
        'command': [
            '/usr/local/bin/websockify', '--web', '/usr/share/novnc', '5901', '--', 'vncserver', '-verbose', '-xstartup', 'startlxde', '-SecurityTypes', 'None', '-geometry', '1024x768', '-fg', ':1'],
        'absolute_url': False,
        'environment': {
            'PATH': '/usr/local/bin:/usr/bin:/bin',
        },
        'port': 5901,
        'timeout': 30,
        'indexpage': 'vnc.html?autoconnect=true',
    }
}
