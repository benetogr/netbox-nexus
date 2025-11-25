from django.db import models
from netbox.models import NetBoxModel

class NetdiscoConfig(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField(verbose_name="Netdisco URL")
    api_key = models.CharField(max_length=200, blank=True)
    db_host = models.CharField(max_length=200, blank=True)
    db_name = models.CharField(max_length=200, blank=True)
    db_user = models.CharField(max_length=200, blank=True)
    db_password = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Netdisco Configuration"

    def __str__(self):
        return self.name

class CUCMConfig(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    axl_url = models.URLField(verbose_name="AXL URL")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    version = models.CharField(max_length=20, default="12.5")
    verify_ssl = models.BooleanField(default=False, verbose_name="Verify SSL")

    class Meta:
        verbose_name = "CUCM Configuration"

    def __str__(self):
        return self.name

class LDAPConfig(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    server_uri = models.CharField(max_length=200, verbose_name="Server URI")
    bind_dn = models.CharField(max_length=200, verbose_name="Bind DN")
    bind_password = models.CharField(max_length=200)
    search_base = models.CharField(max_length=200)

    class Meta:
        verbose_name = "LDAP Configuration"

    def __str__(self):
        return self.name

class SyncLog(NetBoxModel):
    source = models.CharField(max_length=50)  # Netdisco, CUCM, LDAP
    status = models.CharField(max_length=20)  # Success, Failed
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.source} - {self.status} at {self.timestamp}"
