FROM jupyter/base-notebook

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
RUN apt-get install -y -q \
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
RUN /opt/conda/bin/pip install https://github.com/manics/jupyter-server-proxy/archive/indexpage.zip
RUN conda install -y -q -c manics websockify=0.9.0
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py

# There may be a discrepency between the interface vncserver listens on
# (127.0.0.1) and the interface jupyter-server-proxy connects to (localhost)
# https://bugzilla.redhat.com/show_bug.cgi?id=895582
RUN sed -i.bak s/localhost/127.0.0.1/g /opt/conda/lib/python3.7/site-packages/jupyter_server_proxy/handlers.py

WORKDIR ${HOME}

# Both these should work:
# http://127.0.0.1:8888/desktop
# http://localhost:5901/vnc.html
