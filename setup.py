from setuptools import setup, find_packages


setup(
    name="jupyter-desktop-server",
    packages=find_packages(),
    version='0.1.2',
    entry_points={
        'jupyter_serverproxy_servers': [
            'desktop = jupyter_desktop:setup_desktop',
        ]
    },
    install_requires=['jupyter-server-proxy'],
    include_package_data=True,
    zip_safe=False
)
