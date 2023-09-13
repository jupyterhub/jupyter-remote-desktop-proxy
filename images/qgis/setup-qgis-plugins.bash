#!/bin/bash
# Sets up various QGIS plugins that are useful when running
# on the cloud
set -euo pipefail

# First, let's install the plugin manager
# Install from pip until https://github.com/conda-forge/staged-recipes/pull/23971
# is merged and available from `conda-forge`
pip install --no-cache qgis-plugin-manager

# Tell qgis-plugin-manager where our qgis plugins are
export QGIS_PLUGINPATH=/opt/conda/share/qgis/python/plugins

# Initialize the qgis plugin manager
qgis-plugin-manager init
qgis-plugin-manager update

# Install the STAC API Browser plugin: https://stac-utils.github.io/qgis-stac-plugin/
qgis-plugin-manager install "STAC API Browser"
