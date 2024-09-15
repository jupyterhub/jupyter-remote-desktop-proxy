# Jupyter Remote Desktop Proxy

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jupyterhub/jupyter-remote-desktop-proxy/HEAD?urlpath=desktop)
[![Test](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/actions/workflows/test.yaml/badge.svg)](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/actions/workflows/test.yaml)
[![Latest PyPI version](https://img.shields.io/pypi/v/jupyter-remote-desktop-proxy?logo=pypi)](https://pypi.python.org/pypi/jupyter-remote-desktop-proxy)
[![Issue tracking - GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/jupyterhub/jupyter-remote-desktop-proxy/issues)
[![Help forum - Discourse](https://img.shields.io/badge/help_forum-discourse-blue?logo=discourse)](https://discourse.jupyter.org/c/jupyterhub)

Run XFCE (or other desktop environments) on Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc.

When this extension is launched it will run a Linux desktop on the Jupyter single-user server, and proxy it to your browser using VNC via Jupyter.

![Screenshot of jupyter-remote-desktop-proxy XFCE desktop](https://raw.githubusercontent.com/jupyterhub/jupyter-remote-desktop-proxy/main/tests/reference/desktop.png)

## VNC Server

This extension requires a [VNC Server](https://en.wikipedia.org/wiki/Virtual_Network_Computing)
to be installed on the system (likely, in the container image). The
most tested VNC server is [TigerVNC](https://tigervnc.org/), while
[TurboVNC](https://www.turbovnc.org/) also works. Any VNC server available
in `$PATH` as `vncserver` will be used, but no real testing outside of
these servers has been performed.

For an example, see the [`Dockerfile`](./Dockerfile) in this repository which installs TigerVNC and XFCE4.

## Installation

1. Install this package itself, with `pip` from `PyPI`:

   ```bash
   pip install jupyter-remote-desktop-proxy
   ```

2. Install the packages needed to provide a VNC server and the actual Linux Desktop environment.
   You need to pick a desktop environment (there are many!) - here are the packages
   to use TigerVNC and the light-weight [XFCE4](https://www.xfce.org/) desktop environment on Ubuntu 22.04:

   ```
   dbus-x11
   xfce4
   xfce4-panel
   xfce4-session
   xfce4-settings
   xorg
   xubuntu-icon-theme
   tigervnc-standalone-server
   tigervnc-xorg-extension
   ```

   The recommended way to install these is from your Linux system package manager
   of choice (such as apt).

## Docker

To spin up such a notebook first build the container:

```bash
$ docker build -t $(whoami)/$(basename ${PWD}) .
```

Now you can run the image:

```bash
$ docker run --rm --security-opt seccomp=unconfined -p 8888:8888 $(whoami)/$(basename ${PWD})
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

Note the `--security-opt seccomp=unconfined` parameter - this is necessary
to start daemons (such as dbus, pulseaudio, etc) necessary for linux desktop
to work. This is the option kubernetes runs with by default, so most kubernetes
based JupyterHubs will not need any modifications for this to work.

## Limitations

1. Desktop applications that require access to OpenGL are currently unsupported.
