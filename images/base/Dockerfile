ARG BASE_CONTAINER=jupyter/minimal-notebook
FROM $BASE_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY setup-scripts /opt/setup-scripts/

USER root

# Set DISPLAY env variable, so processes know where to open GUI windows.
# Allows python processes running in notebooks to open windows in the GUI.
ENV DISPLAY=":1.0"

# Setup Linux Desktop
RUN /opt/setup-scripts/setup-linux-desktop.bash

COPY startup-scripts /usr/local/bin/start-notebook.d/

# env variables used by downstream images for setting up desktop files or
# mime associations. Consumed by the startup-scripts in startup-scripts/
ENV DESKTOP_FILES_DIR /opt/desktop-files
ENV MIME_FILES_DIR /opt/mime-files
RUN mkdir -p ${DESKTOP_FILES_DIR} ${MIME_FILES_DIR}

USER ${NB_UID}