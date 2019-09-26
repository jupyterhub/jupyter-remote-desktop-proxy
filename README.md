# Jupyter LXDE

Example of running LXDE with noVNC inside Jupyter.

```
docker build -t jupyter-lxde .
docker run -it --rm -p 8888:8888 jupyter-lxde jupyter notebook --debug
```
Go to `/lxde` e.g. http://localhost:8888/lxde and if you're lucky you'll see the LXDE desktop.
