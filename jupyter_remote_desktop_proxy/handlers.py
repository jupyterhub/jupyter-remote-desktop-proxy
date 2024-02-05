import os

import jinja2
from jupyter_server.base.handlers import JupyterHandler
from tornado import web

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.join(os.path.dirname(__file__), 'templates')
    ),
)


HERE = os.path.dirname(os.path.abspath(__file__))


class DesktopHandler(JupyterHandler):
    @web.authenticated
    async def get(self):
        template_params = {
            'base_url': self.base_url,
        }
        template_params.update(self.serverapp.jinja_template_vars)
        self.write(jinja_env.get_template("index.html").render(**template_params))
