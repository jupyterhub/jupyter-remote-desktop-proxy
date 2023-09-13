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

Base and all additional inheriting from it have the following additional tags:

1. The UTC date on which the image was built
2. The commit hash of the repo when the image was built
3. The version of the base Ubuntu image used for the image
4. The version of python used for the image

All the available tags can be found [here](https://quay.io/repository/jupyter-remote-desktop-proxy/base?tab=tags)

Child images may have additional tags provided as well, particularly around
the version of the application they provide.

## QGIS image `quay.io/jupyter-remote-desktop-proxy/qgis`

This image is based off the base image, and installs the popular [QGIS](https://qgis.org/en/site/)
application. A desktop launcher icon is provided, along with filetype associations
so users can double click most files that can be opend via QGIS and they will
be!

In addition to the tags provided by the base image, qgis image provides two
additional tags:

1. The _full_ qgis version, such as `qgis-3.31.2`
2. A _partial_ qgis version, such as `qgis-3.31`

All the available tags can be found [here](https://quay.io/repository/jupyter-remote-desktop-proxy/qgis?tab=tags)

QGIS plugins that are deemed useful when working in the cloud are included
by default. This currently includes the following plugins:

1. [QGIS STAC API browser](https://stac-utils.github.io/qgis-stac-plugin/)

However, these are not _enabled_ by default. The user still has to go to the
plugins menu and enable them.

## Policy for adding images

To reduce maintenance burden, we will only accept maintaining images here that
match the following criteria:

1. They add an application with a _popular_ scientific use case.
2. The application is already package and maintained in `conda-forge`.

Users are encouraged to build and maintain their own images where possible,
inheriting from the base image here for ease of use.
