FROM jupyter/base-notebook

USER root
RUN apt-get update -y -q && \
    apt-get install -y -q \
        curl \
        lxde \
        net-tools \
        novnc \
        tigervnc-standalone-server

RUN apt-get install -y -q python-pip
# Force an upgrade https://github.com/novnc/noVNC/issues/1276
RUN /usr/bin/pip install -U websockify==0.9.0
# pip doesn't rebuild rebind.so though so use the old version
RUN ln -s /usr/lib/websockify/rebind.so /usr/local/lib/

# Patch novnc to automatically connect
ADD websocket-path-ui-js.patch /usr/share/novnc/include
RUN cd /usr/share/novnc/include/ && \
    patch -p0 < websocket-path-ui-js.patch

USER jovyan
# Custom jupyter-server-proxy to load vnc.html instead of /
RUN /opt/conda/bin/pip install https://github.com/manics/jupyter-server-proxy/archive/indexpage.zip
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/

# websockify --web /usr/share/novnc 5901 -- vncserver -verbose -xstartup startlxde -SecurityTypes None -geometry 1024x768 -fg :1

# Both these should work:
# http://localhost:5901/vnc.html
# http://127.0.0.1:8888/lxde
