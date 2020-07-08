from setuptools import setup, find_packages


setup(
    name="jupyter-desktop-server",
    packages=find_packages(),
    version='0.1.3',
    entry_points={
        'jupyter_serverproxy_servers': [
            'desktop = jupyter_desktop:setup_desktop',
        ]
    },
    install_requires=['jupyter-server-proxy>=1.4.0'],
    include_package_data=True,
    zip_safe=False
)
