ARG IMAGE_PREFIX
FROM ${IMAGE_PREFIX}base:latest

RUN mamba install -c conda-forge --yes \
    qgis \
    qgis-plugin-manager

COPY --chown=1000:1000 setup-qgis-plugins.bash /tmp/setup-qgis-plugins.bash
RUN /tmp/setup-qgis-plugins.bash && rm /tmp/setup-qgis-plugins.bash

COPY qgis.desktop ${DESKTOP_FILES_DIR}/qgis.desktop
COPY qgis.xml ${MIME_FILES_DIR}/qgis.xml
