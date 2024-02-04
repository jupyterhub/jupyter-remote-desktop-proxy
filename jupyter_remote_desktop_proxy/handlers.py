import os
import shlex
import tempfile
from shutil import which

import jinja2
from jupyter_server_proxy.handlers import SuperviseAndProxyHandler
from tornado import web

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    ),
)


HERE = os.path.dirname(os.path.abspath(__file__))


def get_websockify_command():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')
    vncserver = which('vncserver')

    if vncserver is None:
        # Use bundled tigervnc
        vncserver = os.path.join(HERE, 'share/tigervnc/bin/vncserver')

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

    return (
        [
            'websockify',
            '-v',
            '--heartbeat',
            '30',
            '{port}',
        ]
        + socket_args
        + ['--', '/bin/sh', '-c', f'cd {os.getcwd()} && {vnc_command}']
    )


class DesktopHandler(SuperviseAndProxyHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = get_websockify_command()

    @web.authenticated
    async def http_get(self, *args, **kwargs):
        template_params = {
            'base_url': self.base_url,
        }
        template_params.update(self.serverapp.jinja_template_vars)
        self.write(jinja_env.get_template("index.html").render(**template_params))
