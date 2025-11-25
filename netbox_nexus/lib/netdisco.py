import psycopg2
from django.utils import timezone
from dcim.models import Device, DeviceType, Manufacturer, Site, DeviceRole
from ..models import NetdiscoConfig, SyncLog

class NetdiscoSync:
    def __init__(self, config: NetdiscoConfig):
        self.config = config
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.config.db_host,
            database=self.config.db_name,
            user=self.config.db_user,
            password=self.config.db_password
        )

    def close(self):
        if self.conn:
            self.conn.close()

    def sync_devices(self):
        log = SyncLog(source="Netdisco", status="Running", message="Starting sync...")
        log.save()
        
        try:
            self.connect()
            cursor = self.conn.cursor()
            
            # Basic query to get devices. Adjust fields based on actual Netdisco schema version.
            # Assuming 'device' table has ip, name, vendor, model, serial, location
            cursor.execute("SELECT ip, name, vendor, model, serial, location FROM device")
            devices = cursor.fetchall()
            
            synced_count = 0
            
            # Ensure a default site and role exist for new devices
            default_site, _ = Site.objects.get_or_create(name="Netdisco Discovered", slug="netdisco-discovered")
            default_role, _ = DeviceRole.objects.get_or_create(name="Discovered", slug="discovered")

            for row in devices:
                ip, name, vendor, model, serial, location = row
                
                # Handle Manufacturer
                if not vendor:
                    vendor = "Unknown"
                manufacturer, _ = Manufacturer.objects.get_or_create(name=vendor, slug=vendor.lower().replace(" ", "-"))
                
                # Handle Device Type
                if not model:
                    model = "Unknown"
                device_type, _ = DeviceType.objects.get_or_create(
                    manufacturer=manufacturer, 
                    model=model, 
                    slug=model.lower().replace(" ", "-")[:50] # Slug limit
                )
                
                # Handle Device
                # Try to find by Serial first, then Name
                device = None
                if serial:
                    device = Device.objects.filter(serial=serial).first()
                
                if not device and name:
                    device = Device.objects.filter(name=name).first()
                    
                if not device:
                    device = Device(
                        name=name or str(ip),
                        device_type=device_type,
                        role=default_role,
                        site=default_site,
                        serial=serial or '',
                        status='active'
                    )
                else:
                    # Update existing fields if needed
                    device.device_type = device_type
                    device.serial = serial or device.serial
                
                device.save()
                synced_count += 1
                
            log.status = "Success"
            log.message = f"Synced {synced_count} devices."
            log.save()
            
        except Exception as e:
            log.status = "Failed"
            log.message = str(e)
            log.save()
            raise e
        finally:
            self.close()
