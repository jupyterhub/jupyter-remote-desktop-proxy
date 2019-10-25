# Jupyter OMERO/Fiji/Napari Desktop
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/manics/jupyter-omeroanalysis-desktop/napari-binder?filepath=napari.ipynb)


Run [OMERO clients](https://www.openmicroscopy.org/omero/downloads/) and [Napari](http://napari.org/) in a Linux desktop using Jupyter.

This is based on https://github.com/ryanlovett/nbnovnc

Either [run on mybinder.org](https://mybinder.org/v2/gh/manics/jupyter-omeroanalysis-desktop/napari-binder?filepath=napari.ipynb) or build locally with [repo2docker](https://repo2docker.readthedocs.io/):
```
repo2docker .
```

Open the displayed URL, then go to `/desktop` e.g. http://localhost:8888/desktop and if you're lucky you'll see a Linux desktop with icons for OMERO.insight and FIJI.

Once the desktop is open go back to the main Jupyter Notebook window, open `napari.ipynb` and execute the cells one at a time. You should see Napari open in the desktop window.
