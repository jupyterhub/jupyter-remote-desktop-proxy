from setuptools import setup, find_packages


setup(
    name="jupyter-desktop-server",
    packages=find_packages(),
    version='0.1.2',
    entry_points={
        'jupyter_serverproxy_servers': [
            'vnc = jupyter_desktop_server:setup_vnc',
        ]
    },
    data_files=[
        ('etc/jupyter/jupyter_notebook_config.d', ['jupyter_desktop_server/etc/jupyter-desktop-server-serverextension.json']),
    ],
    install_requires=['jupyter-server-proxy>=1.2.0'],
    include_package_data=True,
    zip_safe=False
)
