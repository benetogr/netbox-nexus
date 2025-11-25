# NetBox Nexus Plugin

A NetBox plugin to integrate with Netdisco, CUCM, and LDAP for automatic network discovery and asset synchronization.

## Features

*   **Netdisco Integration**: Sync devices, manufacturers, and device types from your Netdisco database.
*   **CUCM Integration**: Sync VoIP phones from Cisco Unified Communications Manager using AXL.
*   **LDAP Integration**: Sync users from your Active Directory or LDAP server.

## Installation

### Automatic Installation (Linux)

If you have a standard NetBox installation at `/opt/netbox`, you can use the included installation script:

```bash
sudo ./install.sh
```

### Manual Installation

1.  **Activate the NetBox virtual environment**:
    ```bash
    source /opt/netbox/venv/bin/activate
    ```

2.  **Install the plugin**:
    ```bash
    pip install .
    ```

3.  **Configure NetBox**:
    Add `netbox_nexus` to your `PLUGINS` list in `/opt/netbox/netbox/netbox/configuration.py`:
    ```python
    PLUGINS = [
        'netbox_nexus',
    ]
    ```

4.  **Run Migrations**:
    ```bash
    cd /opt/netbox/netbox/
    python3 manage.py migrate
    ```

5.  **Restart NetBox**:
    ```bash
    sudo systemctl restart netbox
    ```

## Configuration

Once installed, go to the **Nexus** menu in NetBox to configure your connections:

*   **Netdisco**: Enter your PostgreSQL database credentials.
*   **CUCM**: Enter your AXL URL (e.g., `https://cucm.example.com:8443/axl/`), username, and password.
*   **LDAP**: Enter your LDAP server URI and bind credentials.
