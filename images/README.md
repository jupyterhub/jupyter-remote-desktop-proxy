# jupyter-remote-desktop-proxy docker images

Setting up docker images that run applications well can be a little
complex, so we provide a simple base image that makes that easy. In
addition, we also provide some simple derived images that have popular
datascience related desktop applications set up correctly and ready to
use.

The images will be published _only_ to [quay.io](https://quay.io/organization/jupyter-remote-desktop-proxy),
to make sure people don't run into pulling limits from Dockerhub.

## Base image `quay.io/jupyter-remote-desktop-proxy/base`

This image is based off the `jupyter/minimal-notebook` image maintained
as part of jupyter/docker-stacks, and adds the following features:

1. The lightweight [XFCE4 desktop environment](https://www.xfce.org/)
2. The [Firefox web browser](https://www.mozilla.org/en-US/firefox/new/)
3. A helper script to setup [.desktop](https://wiki.archlinux.org/title/desktop_entries) files
   correctly, so applications can show up in the Desktop and Application launcher.
4. A helper script to setup [MIME associations](https://wiki.archlinux.org/title/XDG_MIME_Applications)
   correctly, so users can double click certain kinds of files and have them open
   in specific applications.

## QGIS image `quay.io/jupyter-remote-desktop-proxy/qgis`

This image is based off the base image, and installs the popular [QGIS](https://qgis.org/en/site/)
application. A desktop launcher icon is provided, along with filetype associations
so users can double click most files that can be opend via QGIS and they will
be!
