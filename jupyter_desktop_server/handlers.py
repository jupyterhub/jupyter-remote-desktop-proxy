from notebook.base.handlers import IPythonHandler
import jinja2
import os


class DesktopHandler(IPythonHandler):
    def initialize(self):
        super().initialize()
        # FIXME: Is this really the best way to use jinja2 here?
        # I can't seem to get the jinja2 env in the base handler to
        # actually load templates from arbitrary paths ugh.
        jinja2_env = self.settings['jinja2_env']
        jinja2_env.loader = jinja2.ChoiceLoader([
            jinja2_env.loader,
            jinja2.FileSystemLoader(
                os.path.join(os.path.dirname(__file__), 'templates')
            )
        ])

    def get(self):
        novnc_base_url = self.base_url + "desktop-server/static/noVNC-1.1.0/"
        self.write(
            self.render_template('desktop.html', novnc_base_url=novnc_base_url)
        )