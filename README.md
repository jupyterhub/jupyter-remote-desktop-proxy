# Jupyter Linux Desktop
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gist/manics/7d1f4b76ce06c2bb07db88e3496a1561/master?urlpath=desktop)

Example of running a Linux desktop or window manager with noVNC inside Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc

```
docker build -t jupyter-desktop .
docker run -it --rm -p 8888:8888 jupyter-desktop jupyter notebook --debug
```
Go to `/desktop` e.g. http://localhost:8888/desktop and if you're lucky you'll see the desktop you installed.
