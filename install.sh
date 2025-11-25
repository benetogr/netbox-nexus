#!/bin/bash

# NetBox Nexus Plugin Installer
# Assumes standard NetBox installation at /opt/netbox

NETBOX_ROOT="/opt/netbox"
VENV_PATH="$NETBOX_ROOT/venv"
CONFIG_PATH="$NETBOX_ROOT/netbox/netbox/configuration.py"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Installing NetBox Nexus Plugin..."

# 1. Activate Virtual Environment and Install
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    pip install .
else
    echo "Error: NetBox virtual environment not found at $VENV_PATH"
    exit 1
fi

# 2. Add to configuration.py
if grep -q "netbox_nexus" "$CONFIG_PATH"; then
    echo "Plugin already in configuration.py"
else
    echo "Adding plugin to configuration.py..."
    # This is a simple append. For production, manual verification is recommended.
    # We look for the PLUGINS list and try to insert, or append if not found (risky).
    # Safer: Append to local_requirements or just instruct user.
    # Here we will try to append to the PLUGINS list if it exists in a simple format, 
    # otherwise we warn the user.
    
    # Simple approach: Append to end of file if not present (assuming PLUGINS += [...] or similar works, 
    # but standard NetBox uses PLUGINS = [...]).
    # Let's just print a big warning for this step to be safe, or try to sed it.
    
    # Using a safe sed to insert into the PLUGINS list if it exists
    sed -i "/PLUGINS = \[/a \    'netbox_nexus'," "$CONFIG_PATH"
fi

# 3. Run Migrations
echo "Running migrations..."
cd "$NETBOX_ROOT/netbox"
python3 manage.py migrate

# 4. Collect Static (if needed, usually for plugins with static files)
# python3 manage.py collectstatic --no-input

# 5. Restart Services
echo "Restarting NetBox services..."
systemctl restart netbox netbox-rq

echo "Installation Complete!"
echo "Please verify 'netbox_nexus' is in your PLUGINS list in $CONFIG_PATH"
