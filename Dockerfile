FROM jupyter/base-notebook:1386e2046833

USER root
# Useful tools for debugging connection problems
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        net-tools \
        vim

# Desktop environment, keep in sync with jupyter_notebook_config.py
# ENV DESKTOP_PACKAGE lxde
ENV DESKTOP_PACKAGE xfce4
RUN apt-get update -y -q && \
    apt-get install -y -q \
    xterm \
    ${DESKTOP_PACKAGE}

# Don't install distro versions of tigervnc and websockify, instead install
# upstream versions

# Novnc: just want web files
RUN cd /opt && \
    curl -sSfL https://github.com/novnc/noVNC/archive/v1.1.0.tar.gz | tar -zxf -

# Patch novnc to use correct path to websockify (defaults to /)
# Note if you use vnc.html you will need to patch ui.js to use the correct path
# and also to override localstorage which may store an incorrect path from a
# different session
# Also resize server instead of scaling client
RUN sed -i.bak \
    -e "s%\('path', 'websockify'\)%'path', window.location.pathname.replace(/[^/]*$/, '').substring(1) + 'websockify'); console.log('websockify path:' + path%" \
    -re "s%rfb.scaleViewport = .+%rfb.resizeSession = readQueryVariable('resize', true);%" \
    /opt/noVNC-1.1.0/vnc_lite.html

# Install tigervnc to /usr/local
RUN curl -sSfL 'https://bintray.com/tigervnc/stable/download_file?file_path=tigervnc-1.9.0.x86_64.tar.gz' | tar -zxf - -C /usr/local --strip=2

USER jovyan

# Custom jupyter-server-proxy to load vnc_lite.html instead of /
# https://github.com/jupyterhub/jupyter-server-proxy/pull/151
RUN /opt/conda/bin/pip install https://github.com/manics/jupyter-server-proxy/archive/1f22ccf44abd7ab5f7b306d57b6adb1dc3190e8b.zip
RUN conda install -y -q -c manics websockify=0.9.0

ADD jupyter_notebook_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py


########## Applications

USER root
RUN apt-get update -y -q && \
    apt-get install -y -q \
    firefox \
    less \
    openjdk-8-jre \
    unzip
# default-jre is java 11 which is incompatible with Fiji

USER jovyan
RUN wget -q https://downloads.imagej.net/fiji/latest/fiji-nojre.zip && \
    unzip -q fiji-nojre.zip && \
    echo TODO: rm fiji-nojre.zip
RUN wget -q https://github.com/ome/omero-insight/releases/download/v5.5.6/OMERO.imagej-5.5.6.zip && \
    cd Fiji.app/plugins && \
    unzip -q ../../OMERO.imagej-5.5.6.zip && \
    echo TODO: rm OMERO.imagej-5.5.6.zip

RUN wget -q https://github.com/ome/omero-insight/releases/download/v5.5.6/OMERO.insight-5.5.6.zip && \
    unzip -q OMERO.insight-5.5.6.zip && \
    echo TODO: rm OMERO.insight-5.5.6.zip

RUN mkdir .java && \
    cd OMERO.insight-5.5.6 && \
    wget -q https://www.openmicroscopy.org/img/logos/omero-logomark.svg
# https://developer.gnome.org/desktop-entry-spec/
#COPY --chown=${NB_UID}:${NB_GID} *.desktop /home/jovyan/Desktop/
COPY --chown=1000:100 *.desktop /home/jovyan/Desktop/
# Configure default OMERO.insight server list
#COPY --chown=${NB_UID}:${NB_GID} java_userPrefs .java/.userPrefs
COPY --chown=1000:100 java_userPrefs .java/.userPrefs

WORKDIR ${HOME}

# Both these should work:
# http://127.0.0.1:8888/desktop
# http://localhost:5901/vnc.html
