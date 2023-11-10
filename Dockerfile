FROM quay.io/jupyter/base-notebook:latest

USER root

RUN apt-get -y -qq update \
 && apt-get -y -qq install \
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
    # Create /opt/install to ensure it's writable by pip
 && mkdir -p /opt/install \
 && chown -R $NB_UID:$NB_GID $HOME /opt/install \
 && rm -rf /var/lib/apt/lists/*

USER $NB_USER

COPY --chown=$NB_UID:$NB_GID jupyter_remote_desktop_proxy /opt/install/jupyter_remote_desktop_proxy
COPY --chown=$NB_UID:$NB_GID environment.yml setup.py MANIFEST.in README.md LICENSE /opt/install/

RUN cd /opt/install && \
    . /opt/conda/bin/activate && \
    mamba env update --quiet --file environment.yml
