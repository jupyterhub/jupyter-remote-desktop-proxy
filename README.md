# Jupyter Desktop Server
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yuvipanda/jupyter-desktop-server/master?urlpath=desktop)

Run XFCE (or other desktop environments) on a JupyterHub.

This is based on https://github.com/ryanlovett/nbnovnc and a fork of https://github.com/manics/jupyter-omeroanalysis-desktop


## Docker 

To spin up such a notebook, please build and run the container like this.

```bash
$ docker build -t $(whoami)/$(basename ${PWD}) .
Sending build context to Docker daemon  36.76MB
Step 1/5 : FROM jupyter/datascience-notebook:latest
**snip**
Successfully installed aiohttp-3.6.2 async-timeout-3.0.1 jupyter-desktop-server-0.1.2 jupyter-server-proxy-1.5.0 multidict-4.7.6 simpervisor-0.3 yarl-1.4.2
Removing intermediate container ed906d6b1074
 ---> 826211e74ce1
Successfully built 826211e74ce1
Successfully tagged myname/jupyter-desktop-server:latest
$ 
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