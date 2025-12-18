#!/bin/bash

set -e

SYSTEMD_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
DATA_DIR="$DATA_HOME/it.mijorus.smile"

# Create the directory if it doesn't exist
mkdir -p $DATA_DIR

# Create the smile-autopaste.sh script
cat > "$DATA_DIR/smile-autopaste.sh" << 'EOF'
#!/bin/bash

# Monitor D-Bus signals and trigger dotool command
dbus-monitor --session "type='signal',interface='it.mijorus.smile',member='CopiedEmojiBroadcast',path='/it/mijorus/smile/actions'" | \
while read -r line; do
    if echo "$line" | grep -q "member=CopiedEmojiBroadcast"; then
        if ! which dotool &> /dev/null; then
            echo "Error: dotool is not installed or not in PATH" >&2
            continue
        fi

        # Trigger the dotool command
        echo 'key ctrl+shift+v' | dotool
    fi
done
EOF

# Make the script executable
chmod +x "$DATA_DIR/smile-autopaste.sh"

# Create systemd user service directory if it doesn't exist
mkdir -p $SYSTEMD_USER_DIR

# Create the systemd service file
cat > "$SYSTEMD_USER_DIR/smile-autopaste.service" << 'EOF'
[Unit]
Description=Smile Autopaste Service for Smile
After=graphical-session.target

[Service]
Type=simple
ExecStart=$DATA_DIR/smile-autopaste.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Reload systemd user daemon
systemctl --user daemon-reload

# Enable and start the service
systemctl --user enable smile-autopaste.service
systemctl --user start smile-autopaste.service