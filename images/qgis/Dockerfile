ARG IMAGE_PREFIX
FROM ${IMAGE_PREFIX}base:latest

RUN mamba install -c conda-forge --yes \
    qgis

COPY qgis.desktop ${DESKTOP_FILES_DIR}/qgis.desktop
COPY qgis.xml ${MIME_FILES_DIR}/qgis.xml
