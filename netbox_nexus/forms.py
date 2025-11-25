from django import forms
from netbox.forms import NetBoxModelForm
from .models import NetdiscoConfig, CUCMConfig, LDAPConfig

class NetdiscoConfigForm(NetBoxModelForm):
    class Meta:
        model = NetdiscoConfig
        fields = ('name', 'base_url', 'api_key', 'db_host', 'db_name', 'db_user', 'db_password', 'tags')
        widgets = {
            'db_password': forms.PasswordInput(),
            'api_key': forms.PasswordInput(),
        }

class CUCMConfigForm(NetBoxModelForm):
    class Meta:
        model = CUCMConfig
        fields = ('name', 'axl_url', 'username', 'password', 'version', 'verify_ssl', 'tags')
        widgets = {
            'password': forms.PasswordInput(),
        }

class LDAPConfigForm(NetBoxModelForm):
    class Meta:
        model = LDAPConfig
        fields = ('name', 'server_uri', 'bind_dn', 'bind_password', 'search_base', 'tags')
        widgets = {
            'bind_password': forms.PasswordInput(),
        }
