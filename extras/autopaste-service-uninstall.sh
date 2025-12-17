#!/bin/bash

set -e

SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DATA_DIR="$DATA_HOME/it.mijorus.smile"

echo 'Removing systemd service...'
systemctl --user stop smile-autopaste.service
systemctl --user disable smile-autopaste.service

echo "Removing $DATA_DIR directory..."
rm -r $DATA_DIR

echo 'Done'