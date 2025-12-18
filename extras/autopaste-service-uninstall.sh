#!/bin/bash

set -e

SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DATA_DIR="$DATA_HOME/it.mijorus.smile"
AUTOPASTE_SCRIPT_LOCATION="$DATA_DIR/smile-autopaste.sh"
SERVICE_NAME="smile-autopaste.service"

echo 'Removing systemd service...'
systemctl --user stop $SERVICE_NAME
systemctl --user disable $SERVICE_NAME

echo "Removing $AUTOPASTE_SCRIPT_LOCATION..."
rm -rf "$AUTOPASTE_SCRIPT_LOCATION"

echo "$SERVICE_NAME successfully removed."