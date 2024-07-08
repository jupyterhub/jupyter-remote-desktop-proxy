import os
from subprocess import check_call

from setuptools import find_packages, setup
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
    packages=find_packages(),
    version='2.0.2.dev',
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
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
    include_package_data=True,
    keywords=["Interactive", "Desktop", "Jupyter"],
    license="BSD",
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
