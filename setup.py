import os
from subprocess import check_call

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

HERE = os.path.dirname(__file__)


def webpacked_command(command):
    """
    Return a command that inherits from command, but adds webpack JS building
    """

    class WebPackedCommand(command):
        """
        Run npm webpack to generate appropriate output files before given command.

        This generates all the js & css we need, and that is included via an
        entry in MANIFEST.in
        """

        description = "build frontend files with webpack"

        def run(self):
            """
            Call npm install & npm run webpack before packaging
            """
            check_call(
                ["npm", "install", "--progress=false", "--unsafe-perm"],
                cwd=HERE,
            )

            check_call(["npm", "run", "webpack"], cwd=HERE)

            return super().run()

    return WebPackedCommand


with open("README.md") as f:
    readme = f.read()


setup(
    name="jupyter-remote-desktop-proxy",
    packages=["jupyter_remote_desktop_proxy"],
    version='3.0.2.dev0',
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    description="Run a desktop environments on Jupyter",
    entry_points={
        'jupyter_serverproxy_servers': [
            'desktop-websockify = jupyter_remote_desktop_proxy.setup_websockify:setup_websockify',
        ]
    },
    install_requires=[
        'jupyter-server-proxy>=4.3.0',
    ],
    package_data={
        "jupyter_remote_desktop_proxy": [
            "share/*",
            "static/*",
            "static/dist/*",
            "templates/*",
        ],
    },
    keywords=["Interactive", "Desktop", "Jupyter"],
    license="BSD-3-Clause",
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms="Linux",
    project_urls={
        "Source": "https://github.com/jupyterhub/jupyter-remote-desktop-proxy/",
        "Tracker": "https://github.com/jupyterhub/jupyter-remote-desktop-proxy/issues",
    },
    python_requires=">=3.8",
    url="https://jupyter.org",
    zip_safe=False,
    cmdclass={
        # Handles making sdists and wheels
        "sdist": webpacked_command(sdist),
        # Handles `pip install` directly
        "build_py": webpacked_command(build_py),
    },
    data_files=[
        (
            'etc/jupyter/jupyter_server_config.d',
            [
                'jupyter-config/jupyter_server_config.d/jupyter_remote_desktop_proxy.json'
            ],
        ),
        (
            'etc/jupyter/jupyter_notebook_config.d',
            [
                'jupyter-config/jupyter_notebook_config.d/jupyter_remote_desktop_proxy.json'
            ],
        ),
    ],
)
