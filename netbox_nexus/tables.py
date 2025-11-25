import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import NetdiscoConfig, CUCMConfig, LDAPConfig, SyncLog

class NetdiscoConfigTable(NetBoxTable):
    name = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = NetdiscoConfig
        fields = ('pk', 'id', 'name', 'base_url', 'db_host', 'actions')
        default_columns = ('name', 'base_url', 'db_host')

class CUCMConfigTable(NetBoxTable):
    name = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = CUCMConfig
        fields = ('pk', 'id', 'name', 'axl_url', 'version', 'verify_ssl', 'actions')
        default_columns = ('name', 'axl_url', 'version')

class LDAPConfigTable(NetBoxTable):
    name = tables.Column(linkify=True)
    
    class Meta(NetBoxTable.Meta):
        model = LDAPConfig
        fields = ('pk', 'id', 'name', 'server_uri', 'bind_dn', 'actions')
        default_columns = ('name', 'server_uri', 'bind_dn')

class SyncLogTable(NetBoxTable):
    source = tables.Column(linkify=True)
    timestamp = columns.DateTimeColumn()
    
    class Meta(NetBoxTable.Meta):
        model = SyncLog
        fields = ('pk', 'id', 'source', 'status', 'message', 'timestamp', 'actions')
        default_columns = ('source', 'status', 'message', 'timestamp')
