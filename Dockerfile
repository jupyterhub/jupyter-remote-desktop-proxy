FROM jupyter/base-notebook

USER root
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        patch \
        tigervnc-standalone-server \
        vim
RUN apt-get install -y -q \
        lxde


# Novnc: just want web files, we'll install our own newer websockify
RUN apt-get download -q novnc && \
    dpkg --force-all -i novnc*.deb && \
    rm novnc*.deb
# Patch novnc to automatically connect
# Download missing fonts
ADD websocket-path-ui-js.patch /usr/share/novnc/include
RUN cd /usr/share/novnc/include/ && \
    patch -p0 < websocket-path-ui-js.patch && \
    curl -sSfLO https://raw.githubusercontent.com/novnc/noVNC/v1.1.0/app/styles/Orbitron700.ttf && \
    curl -sSfLO https://raw.githubusercontent.com/novnc/noVNC/v1.1.0/app/styles/Orbitron700.woff

USER jovyan
# Custom jupyter-server-proxy to load vnc.html instead of /
RUN /opt/conda/bin/pip install https://github.com/manics/jupyter-server-proxy/archive/indexpage.zip
RUN conda install -y -q -c manics/label/testing websockify
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py

# There may be a discrepency between the interface vncserver listens on
# (127.0.0.1) and the interface jupyter-server-proxy connects to (localhost)
# https://bugzilla.redhat.com/show_bug.cgi?id=895582
RUN sed -i.bak s/localhost/127.0.0.1/g /opt/conda/lib/python3.7/site-packages/jupyter_server_proxy/handlers.py

# Both these should work:
# http://localhost:5901/vnc.html
# http://127.0.0.1:8888/lxde
