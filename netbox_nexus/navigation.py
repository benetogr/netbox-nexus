from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_nexus:netdiscoconfig_list',
        link_text='Netdisco',
    ),
    PluginMenuItem(
        link='plugins:netbox_nexus:cucmconfig_list',
        link_text='CUCM',
    ),
    PluginMenuItem(
        link='plugins:netbox_nexus:ldapconfig_list',
        link_text='LDAP',
    ),
    PluginMenuItem(
        link='plugins:netbox_nexus:synclog_list',
        link_text='Sync Logs',
    ),
)
