from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()


setup(
    name="jupyter-desktop-server",
    packages=find_packages(),
    version='0.1.3',
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
            'desktop = jupyter_desktop:setup_desktop',
        ]
    },
    install_requires=['jupyter-server-proxy>=1.4.0'],
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
    python_requires=">=3.6",
    url="https://jupyter.org",
    zip_safe=False
)
