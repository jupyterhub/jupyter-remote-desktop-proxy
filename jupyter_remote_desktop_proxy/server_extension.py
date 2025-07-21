import os
from pathlib import Path

from jupyter_server.base.handlers import AuthenticatedFileHandler
from jupyter_server.utils import url_path_join
from jupyter_server_proxy.handlers import AddSlashHandler

from .handlers import DesktopHandler

HERE = Path(__file__).parent


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]

    jupyter_remote_desktop_endpoints = os.getenv('JUPYTER_REMOTE_DESKTOP_ENDPOINTS', '')
    endpoints = ['desktop'] + jupyter_remote_desktop_endpoints.split(',')
    for endpoint in endpoints:
        server_app.web_app.add_handlers(
            ".*",
            [
                # Serve our own static files
                (
                    url_path_join(base_url, f"/{endpoint}/static/(.*)"),
                    AuthenticatedFileHandler,
                    {"path": (str(HERE / "static"))},
                ),
                # To simplify URL mapping, we make sure that /desktop/ always
                # has a trailing slash
                (url_path_join(base_url, f"/{endpoint}"), AddSlashHandler),
                (url_path_join(base_url, f"/{endpoint}/"), DesktopHandler),
            ],
        )
