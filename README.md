# Jupyter OMERO client Desktop
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/manics/jupyter-omeroanalysis-desktop/napari-binder?filepath=napari.ipynb)


Run [OMERO clients](https://www.openmicroscopy.org/omero/downloads/) and [Napari](http://napari.org/) in a Linux desktop using Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc

```
docker build -t jupyter-omeroanalysis-desktop .
docker run -it --rm -p 8888:8888 jupyter-omeroanalysis-desktop
```

Open the displayed URL, then go to `/desktop` e.g. http://localhost:8888/desktop and if you're lucky you'll see a Linux desktop with icons for OMERO.insight and FIJI.

Once the desktop is open go back to the main Jupyter Notebook window, open `napari.ipynb` and execute the cells one at a time. You should see Napari open in the desktop window.
