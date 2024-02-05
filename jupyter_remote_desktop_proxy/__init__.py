import os

from .server_extension import load_jupyter_server_extension

HERE = os.path.dirname(os.path.abspath(__file__))


def _jupyter_server_extension_points():
    """
    Set up the server extension for collecting metrics
    """
    return [{"module": "jupyter_remote_desktop_proxy"}]


# For backward compatibility
_load_jupyter_server_extension = load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
