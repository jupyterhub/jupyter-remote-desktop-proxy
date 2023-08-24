#!/bin/bash -l
set -euo pipefail
# This script is run on container startup, as a non-root user
# It copies any .xml files it may find in a MIME_FILES_DIR to the user's
# mime associations directory, allowing image authors to allow users to launch
# a specific application by double clicking files of a specific type.
# It's done at startup time because $HOME is often mounted over by a
# persistent remote filesystem, hiding whatever is in the directory.

# Set nullglob, so we don't error out if there are no MIME files to be found
shopt -s nullglob

MIME_DIR="${HOME}/.local/share/mime"
MIME_PACKAGES_DIR="${MIME_DIR}/packages"
mkdir -p "${MIME_PACKAGES_DIR}"
for mime_file_path in ${MIME_FILES_DIR}/*.xml; do
    cp "${mime_file_path}" "${MIME_PACKAGES_DIR}/."
done
update-mime-database "${MIME_DIR}"
