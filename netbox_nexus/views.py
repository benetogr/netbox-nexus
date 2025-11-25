from django.shortcuts import render, redirect
from django.contrib import messages
from netbox.views import generic
from .models import NetdiscoConfig, CUCMConfig, LDAPConfig, SyncLog
from .forms import NetdiscoConfigForm, CUCMConfigForm, LDAPConfigForm

# Netdisco
class NetdiscoConfigListView(generic.ObjectListView):
    queryset = NetdiscoConfig.objects.all()

class NetdiscoConfigView(generic.ObjectView):
    queryset = NetdiscoConfig.objects.all()

class NetdiscoConfigEditView(generic.ObjectEditView):
    queryset = NetdiscoConfig.objects.all()
    form = NetdiscoConfigForm

class NetdiscoConfigDeleteView(generic.ObjectDeleteView):
    queryset = NetdiscoConfig.objects.all()

class NetdiscoSyncView(generic.ObjectView):
    queryset = NetdiscoConfig.objects.all()
    template_name = 'netbox_nexus/netdiscoconfig_sync.html'

    def get(self, request, pk):
        instance = self.get_object(pk=pk)
        return render(request, self.template_name, {
            'object': instance,
        })

    def post(self, request, pk):
        instance = self.get_object(pk=pk)
        from .lib.netdisco import NetdiscoSync
        try:
            syncer = NetdiscoSync(instance)
            syncer.sync_devices()
            messages.success(request, "Netdisco sync completed successfully.")
        except Exception as e:
            messages.error(request, f"Netdisco sync failed: {e}")
        
        return redirect('plugins:netbox_nexus:netdiscoconfig', pk=pk)


# CUCM
class CUCMConfigListView(generic.ObjectListView):
    queryset = CUCMConfig.objects.all()

class CUCMConfigView(generic.ObjectView):
    queryset = CUCMConfig.objects.all()

class CUCMConfigEditView(generic.ObjectEditView):
    queryset = CUCMConfig.objects.all()
    form = CUCMConfigForm

class CUCMConfigDeleteView(generic.ObjectDeleteView):
    queryset = CUCMConfig.objects.all()

class CUCMSyncView(generic.ObjectView):
    queryset = CUCMConfig.objects.all()
    template_name = 'netbox_nexus/cucmconfig_sync.html'

    def get(self, request, pk):
        instance = self.get_object(pk=pk)
        return render(request, self.template_name, {
            'object': instance,
        })

    def post(self, request, pk):
        instance = self.get_object(pk=pk)
        from .lib.cucm import CUCMSync
        try:
            syncer = CUCMSync(instance)
            syncer.sync_phones()
            messages.success(request, "CUCM sync completed successfully.")
        except Exception as e:
            messages.error(request, f"CUCM sync failed: {e}")
        
        return redirect('plugins:netbox_nexus:cucmconfig', pk=pk)


# LDAP
class LDAPConfigListView(generic.ObjectListView):
    queryset = LDAPConfig.objects.all()

class LDAPConfigView(generic.ObjectView):
    queryset = LDAPConfig.objects.all()

class LDAPConfigEditView(generic.ObjectEditView):
    queryset = LDAPConfig.objects.all()
    form = LDAPConfigForm

class LDAPConfigDeleteView(generic.ObjectDeleteView):
    queryset = LDAPConfig.objects.all()

class LDAPSyncView(generic.ObjectView):
    queryset = LDAPConfig.objects.all()
    template_name = 'netbox_nexus/ldapconfig_sync.html'

    def get(self, request, pk):
        instance = self.get_object(pk=pk)
        return render(request, self.template_name, {
            'object': instance,
        })

    def post(self, request, pk):
        instance = self.get_object(pk=pk)
        from .lib.ldap_sync import LDAPSync
        try:
            syncer = LDAPSync(instance)
            syncer.sync_users()
            messages.success(request, "LDAP sync completed successfully.")
        except Exception as e:
            messages.error(request, f"LDAP sync failed: {e}")
        
        return redirect('plugins:netbox_nexus:ldapconfig', pk=pk)


# Logs
class SyncLogListView(generic.ObjectListView):
    queryset = SyncLog.objects.all()

class SyncLogView(generic.ObjectView):
    queryset = SyncLog.objects.all()
