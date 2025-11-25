from django.urls import path
from . import views
from netbox.views.generic import ObjectChangeLogView
from .models import NetdiscoConfig, CUCMConfig, LDAPConfig, SyncLog

urlpatterns = [
    # Netdisco
    path('netdisco/', views.NetdiscoConfigListView.as_view(), name='netdiscoconfig_list'),
    path('netdisco/add/', views.NetdiscoConfigEditView.as_view(), name='netdiscoconfig_add'),
    path('netdisco/<int:pk>/', views.NetdiscoConfigView.as_view(), name='netdiscoconfig'),
    path('netdisco/<int:pk>/edit/', views.NetdiscoConfigEditView.as_view(), name='netdiscoconfig_edit'),
    path('netdisco/<int:pk>/delete/', views.NetdiscoConfigDeleteView.as_view(), name='netdiscoconfig_delete'),
    path('netdisco/<int:pk>/sync/', views.NetdiscoSyncView.as_view(), name='netdiscoconfig_sync'),
    path('netdisco/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='netdiscoconfig_changelog', kwargs={'model': NetdiscoConfig}),

    # CUCM
    path('cucm/', views.CUCMConfigListView.as_view(), name='cucmconfig_list'),
    path('cucm/add/', views.CUCMConfigEditView.as_view(), name='cucmconfig_add'),
    path('cucm/<int:pk>/', views.CUCMConfigView.as_view(), name='cucmconfig'),
    path('cucm/<int:pk>/edit/', views.CUCMConfigEditView.as_view(), name='cucmconfig_edit'),
    path('cucm/<int:pk>/delete/', views.CUCMConfigDeleteView.as_view(), name='cucmconfig_delete'),
    path('cucm/<int:pk>/sync/', views.CUCMSyncView.as_view(), name='cucmconfig_sync'),
    path('cucm/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='cucmconfig_changelog', kwargs={'model': CUCMConfig}),

    # LDAP
    path('ldap/', views.LDAPConfigListView.as_view(), name='ldapconfig_list'),
    path('ldap/add/', views.LDAPConfigEditView.as_view(), name='ldapconfig_add'),
    path('ldap/<int:pk>/', views.LDAPConfigView.as_view(), name='ldapconfig'),
    path('ldap/<int:pk>/edit/', views.LDAPConfigEditView.as_view(), name='ldapconfig_edit'),
    path('ldap/<int:pk>/delete/', views.LDAPConfigDeleteView.as_view(), name='ldapconfig_delete'),
    path('ldap/<int:pk>/sync/', views.LDAPSyncView.as_view(), name='ldapconfig_sync'),
    path('ldap/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='ldapconfig_changelog', kwargs={'model': LDAPConfig}),

    # Logs
    path('logs/', views.SyncLogListView.as_view(), name='synclog_list'),
    path('logs/<int:pk>/', views.SyncLogView.as_view(), name='synclog'),
]
