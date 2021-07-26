FROM jupyter/base-notebook

USER root

RUN apt-get -y -q update \
 && apt-get -y -q upgrade \
 && apt-get -y -q install \
        dbus-x11 \
        firefox \
        xfce4 \
        xfce4-panel \
        xfce4-session \
        xfce4-settings \
        xorg \
        xubuntu-icon-theme \
    # chown $HOME to workaround that the xorg installation creates a
    # /home/jovyan/.cache directory owned by root
 && chown -R $NB_UID:$NB_GID $HOME \
 && rm -rf /var/lib/apt/lists/*

# Install TurboVNC (https://github.com/TurboVNC/turbovnc)
ARG TURBOVNC_VERSION=2.2.6
RUN wget -q "https://sourceforge.net/projects/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb/download" -O turbovnc.deb \
 && apt-get install -y -q ./turbovnc.deb \
    # remove light-locker to prevent screen lock
 && apt-get remove -y -q light-locker \
 && rm ./turbovnc.deb \
 && ln -s /opt/TurboVNC/bin/* /usr/local/bin/

COPY jupyter_desktop /opt/install/jupyter_desktop
COPY setup.py MANIFEST.in README.md LICENSE /opt/install/
RUN fix-permissions /opt/install

USER $NB_USER
RUN cd /opt/install \
 && mamba install -y websockify \
 && pip install -e .
