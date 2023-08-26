FROM jupyter/base-notebook

USER root

RUN apt-get -y -q update \
 && apt-get -y -q install \
        dbus-x11 \
        xfce4 \
        xfce4-panel \
        xfce4-session \
        xfce4-settings \
        xorg \
        xubuntu-icon-theme \
        tigervnc-standalone-server \
        tigervnc-xorg-extension \
    # chown $HOME to workaround that the xorg installation creates a
    # /home/jovyan/.cache directory owned by root
 && chown -R $NB_UID:$NB_GID $HOME \
 && rm -rf /var/lib/apt/lists/*

USER $NB_USER

RUN mamba install --yes websockify

COPY --chown=$NB_USER:$NB_USER jupyter_remote_desktop_proxy /opt/install/jupyter_remote_desktop_proxy
COPY --chown=$NB_USER:$NB_USER setup.py MANIFEST.in README.md LICENSE /opt/install/

RUN cd /opt/install \
 && pip install -e .
