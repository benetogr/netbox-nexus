from django.db import migrations, models
import taggit.managers
import utilities.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetdiscoConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('base_url', models.URLField(verbose_name='Netdisco URL')),
                ('api_key', models.CharField(blank=True, max_length=200)),
                ('db_host', models.CharField(blank=True, max_length=200)),
                ('db_name', models.CharField(blank=True, max_length=200)),
                ('db_user', models.CharField(blank=True, max_length=200)),
                ('db_password', models.CharField(blank=True, max_length=200)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Netdisco Configuration',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CUCMConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('axl_url', models.URLField(verbose_name='AXL URL')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('version', models.CharField(default='12.5', max_length=20)),
                ('verify_ssl', models.BooleanField(default=False, verbose_name='Verify SSL')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'CUCM Configuration',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='LDAPConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('server_uri', models.CharField(max_length=200, verbose_name='Server URI')),
                ('bind_dn', models.CharField(max_length=200, verbose_name='Bind DN')),
                ('bind_password', models.CharField(max_length=200)),
                ('search_base', models.CharField(max_length=200)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'LDAP Configuration',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SyncLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('source', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
