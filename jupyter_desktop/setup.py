import setuptools


setuptools.setup(
    name="jupyter-desktop-server",
    # py_modules rather than packages, since we only have 1 file
    py_modules=['jupyter_desktop'],
    entry_points={
        'jupyter_serverproxy_servers': [
            'desktop = jupyter_desktop:setup_desktop',
        ]
    },
    install_requires=['jupyter-server-proxy'],
    package_data={
        'jupyter_desktop': ['desktop/*'],
    },
)
