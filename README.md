# Jupyter Linux Desktop

Example of running a Linux desktop or window manager with noVNC inside Jupyter.

```
docker build -t jupyter-desktop .
docker run -it --rm -p 8888:8888 jupyter-desktop jupyter notebook --debug
```
Go to `/desktop` e.g. http://localhost:8888/desktop and if you're lucky you'll see the desktop you installed.
