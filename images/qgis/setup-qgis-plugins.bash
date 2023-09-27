#!/bin/bash
# Sets up various QGIS plugins that are useful when running
# on the cloud
set -euo pipefail

# Tell qgis-plugin-manager where our qgis plugins are
export QGIS_PLUGINPATH=/opt/conda/share/qgis/python/plugins

# Install qgis-stac-plugin from our fork, to add support for reading from S3
git clone https://github.com/slesaad/qgis-stac-plugin
cd qgis-stac-plugin
git checkout support_gdal_assets
pip install --no-cache .

python admin.py build
cp -r build/qgis_stac/ ${QGIS_PLUGINPATH}/qgis_stac/
cd ..
rm -rf qgis-stac-plugin
