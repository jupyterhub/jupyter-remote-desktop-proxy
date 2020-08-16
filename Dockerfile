FROM jupyter/base-notebook:python-3.7.6


USER root

RUN apt-get -y update \
 && apt-get install -y dbus-x11 \
   firefox \
   xfce4 \
   xfce4-panel \
   xfce4-session \
   xfce4-settings \
   xorg \
   xubuntu-icon-theme
# apt-get may result in root-owned directories/files under $HOME
RUN chown -R $NB_UID:$NB_GID $HOME

USER $NB_USER
ADD . /opt/install
RUN cd /opt/install && \
   conda env update -n base --file environment.yml
