# Jupyter Remote Desktop Proxy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyterhub/jupyter-remote-desktop-proxy/HEAD?urlpath=desktop)

Run XFCE (or other desktop environments) on Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc.

When this extension is launched it will run a Linux desktop on the Jupyter single-user server, and proxy it to your browser using VNC via Jupyter.

If a `vncserver` executable is found in `PATH` it will be used, otherwise a bundled TightVNC server is run.
You can use this to install vncserver with support for other features, for example the [`Dockerfile`](./Dockerfile) in this repository installs TurboVNC for improved OpenGL support.

## Installation

1. Install this package itself, with `pip` from `PyPI`:

   ```bash
   pip install jupyter-remote-desktop-proxy
   ```

2. Install the [websockify](https://github.com/novnc/websockify) dependency. Unfortunately,
   the PyPI `websockify` package is broken, so you need to install it either
   from [conda-forge](https://anaconda.org/conda-forge/websockify) or with
   [apt](https://packages.ubuntu.com/search?suite=all&searchon=names&keywords=websockify)

3. Install the packages needed to provide the actual Linux Desktop environment.
   You need to pick a desktop environment (there are many!) - here is the packages
   you would need for using the light-weight [XFCE4](https://www.xfce.org/) desktop environment:

   ```
   dbus-x11
   libgl1-mesa-glx
   xfce4
   xfce4-panel
   xfce4-session
   xfce4-settings
   xorg
   xubuntu-icon-theme
   ```

   The recommended way to install these is from your Linux system package manager
   of choice (such as apt).

## Docker

To spin up such a notebook first build the container:

```bash
$ docker build -t $(whoami)/$(basename ${PWD}) .
```

Now you can ran the image:

```bash
$ docker run --rm  -p 8888:8888 $(whoami)/$(basename ${PWD})
Executing the command: jupyter notebook
[I 12:43:59.148 NotebookApp] Writing notebook server cookie secret to /home/jovyan/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:44:00.221 NotebookApp] JupyterLab extension loaded from /opt/conda/lib/python3.7/site-packages/jupyterlab
[I 12:44:00.221 NotebookApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 12:44:00.224 NotebookApp] Serving notebooks from local directory: /home/jovyan
[I 12:44:00.225 NotebookApp] The Jupyter Notebook is running at:
[I 12:44:00.225 NotebookApp] http://924904e0a646:8888/?token=40475e553b7671b9e93533b97afe584fa2030448505a7d83
[I 12:44:00.225 NotebookApp]  or http://127.0.0.1:8888/?token=40475e553b7671b9e93533b97afe584fa2030448505a7d83
[I 12:44:00.225 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 12:44:00.229 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/nbserver-8-open.html
    Or copy and paste one of these URLs:
        http://924904e0a646:8888/?token=40475e553b7671b9e93533b97afe584fa2030448505a7d83
     or http://127.0.0.1:8888/?token=40475e553b7671b9e93533b97afe584fa2030448505a7d83
*snip*
```

Now head to the URL shown and you will be greated with a XFCE desktop.

## Limitations

1. Desktop applications that require access to OpenGL are currently unsupported.
