#!/bin/bash

# Create the directory if it doesn't exist
mkdir -p ~/.local/share/it.mijorus.smile

# Create the smile-autopaste.sh script
cat > ~/.local/share/it.mijorus.smile/smile-autopaste.sh << 'EOF'
#!/bin/bash
# Monitor D-Bus signals and trigger dotool command
dbus-monitor --session "type='signal',interface='it.mijorus.smile',member='CopiedEmoji',path='/it/mijorus/smile/actions'" | \
while read -r line; do
    # Check if we received the CopiedEmoji signal
    if echo "$line" | grep -q "member=CopiedEmoji"; then
        # Trigger the dotool command
        echo 'key ctrl+shift+v' | dotool
    fi
done
EOF

# Make the script executable
chmod +x ~/.local/share/it.mijorus.smile/smile-autopaste.sh

# Create systemd user service directory if it doesn't exist
mkdir -p ~/.config/systemd/user

# Create the systemd service file
cat > ~/.config/systemd/user/smile-autopaste.service << EOF
[Unit]
Description=Smile Autopaste Service for Smile
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.local/share/it.mijorus.smile/smile-autopaste.sh
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

# Check service status
echo "Service created and started. Status:"
systemctl --user status smile-autopaste.service