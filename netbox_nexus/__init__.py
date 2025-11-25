from netbox.plugins import PluginConfig

class NexusConfig(PluginConfig):
    name = 'netbox_nexus'
    verbose_name = 'NetBox Nexus'
    description = 'Integration with Netdisco, CUCM, and LDAP'
    version = '0.1'
    base_url = 'nexus'
    min_version = '4.0.0'

config = NexusConfig
