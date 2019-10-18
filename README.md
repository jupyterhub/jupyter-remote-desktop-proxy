# Jupyter OMERO client Desktop
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/manics/jupyter-omeroanalysis-desktop/master?urlpath=Desktop)

Run OMERO clients in a Linux desktop using Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc

```
docker build -t jupyter-omeroanalysis-desktop .
docker run -it --rm -p 8888:8888 jupyter-omeroanalysis-desktop
```

Open the displayed URL, then go to `/Desktop` e.g. http://localhost:8888/Desktop and if you're lucky you'll see a Linux desktop with icons for OMERO.insight and FIJI.
