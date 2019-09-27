FROM jupyter/base-notebook

USER root
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        novnc \
        patch \
        tigervnc-standalone-server \
        vim
RUN apt-get install -y -q \
        lxde

# Patch novnc to automatically connect
# Download missing fonts
ADD websocket-path-ui-js.patch /usr/share/novnc/include
RUN cd /usr/share/novnc/include/ && \
    patch -p0 < websocket-path-ui-js.patch && \
    curl -sSfLO https://raw.githubusercontent.com/novnc/noVNC/v1.1.0/app/styles/Orbitron700.ttf && \
    curl -sSfLO https://raw.githubusercontent.com/novnc/noVNC/v1.1.0/app/styles/Orbitron700.woff

# Force remove websockify and install a more recent version
RUN dpkg -r --force-depends websockify

USER jovyan
# Custom jupyter-server-proxy to load vnc.html instead of /
RUN /opt/conda/bin/pip install https://github.com/manics/jupyter-server-proxy/archive/indexpage.zip
RUN conda install -y -q -c manics/label/testing websockify
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/jupyter_notebook_config.py


# Both these should work:
# http://localhost:5901/vnc.html
# http://127.0.0.1:8888/lxde
