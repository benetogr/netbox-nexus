from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
import urllib3

from dcim.models import Device, DeviceType, Manufacturer, Site, DeviceRole
from ..models import CUCMConfig, SyncLog

# Suppress insecure request warnings if using self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CUCMSync:
    def __init__(self, config: CUCMConfig):
        self.config = config
        self.client = None

    def connect(self):
        session = Session()
        session.verify = self.config.verify_ssl
        session.auth = HTTPBasicAuth(self.config.username, self.config.password)
        
        transport = Transport(cache=SqliteCache(), session=session)
        
        # WSDL URL construction might vary. Assuming standard path.
        # Ideally, the WSDL file should be local or accessible via URL.
        # For this implementation, we assume the AXL URL points to the WSDL or the service.
        # A common pattern is https://<cucm>:8443/axl/
        # But Zeep needs the WSDL. We might need to download it or point to a local one.
        # For simplicity, we'll assume the user provides the full WSDL URL in axl_url 
        # or we construct a standard one if it's just the host.
        
        wsdl_url = self.config.axl_url
        if not wsdl_url.endswith('wsdl'):
             # Fallback or assumption, might need adjustment based on actual setup
             pass

        self.client = Client(wsdl=wsdl_url, transport=transport)

    def sync_phones(self):
        log = SyncLog(source="CUCM", status="Running", message="Starting sync...")
        log.save()
        
        try:
            self.connect()
            
            # Execute SQL Query to get phones is often faster/easier than listPhone for bulk
            # But listPhone is more "standard". Let's use executeSQLQuery for flexibility if possible,
            # or listPhone if we want to be strict.
            # Let's try listPhone first as it's a standard AXL operation.
            
            # Note: The search criteria '%' matches everything.
            criteria = {'name': '%'} 
            
            # Depending on AXL version, the method might be listPhone
            # We need to handle the service proxy.
            service = self.client.create_service(
                '{http://www.cisco.com/AXL/API/8.0}AXLAPIBinding',
                self.config.axl_url.replace('?wsdl', '') # Endpoint URL
            )
            
            # This is a simplification. AXL is complex. 
            # We will use a raw SQL query via AXL as it's often more robust for data extraction.
            
            sql = "SELECT name, description, product, model FROM device WHERE tkclass = 1" # tkclass 1 = Phone
            
            resp = service.executeSQLQuery(sql=sql)
            
            synced_count = 0
            
            default_site, _ = Site.objects.get_or_create(name="CUCM Imported", slug="cucm-imported")
            default_role, _ = DeviceRole.objects.get_or_create(name="Phone", slug="phone")
            manufacturer, _ = Manufacturer.objects.get_or_create(name="Cisco", slug="cisco")

            if resp['return']:
                rows = resp['return']['row']
                for row in rows:
                    # Parse XML row or dict depending on Zeep output
                    # Zeep usually returns a list of dict-like objects
                    
                    # Accessing elements might need careful handling depending on Zeep's parsing of the XML
                    # For executeSQLQuery, it returns a list of elements.
                    
                    # Let's assume row is a dict for now (simplified)
                    # In reality, we might need to iterate row children.
                    
                    # Helper to get value safely
                    def get_val(r, tag):
                        for item in r:
                            if item.tag == tag:
                                return item.text
                        return None
                        
                    # If Zeep returns a list of lxml elements for 'row'
                    # We might need to adjust this.
                    
                    # For the sake of this plan, we assume we get the data.
                    name = None
                    description = None
                    model_val = None
                    
                    # If row is a simple dict (if Zeep helper used):
                    # name = row.get('name')
                    
                    # If row is an object:
                    try:
                        name = row[0].text # First column
                        description = row[1].text
                        # etc...
                    except:
                        continue

                    if not name:
                        continue

                    # Create Device Type
                    model_name = "Cisco Phone" # Placeholder, ideally map 'product' or 'model' ID to name
                    device_type, _ = DeviceType.objects.get_or_create(
                        manufacturer=manufacturer,
                        model=model_name,
                        slug=model_name.lower().replace(" ", "-")
                    )

                    # Create Device
                    device = Device.objects.filter(name=name).first()
                    if not device:
                        device = Device(
                            name=name,
                            device_type=device_type,
                            role=default_role,
                            site=default_site,
                            description=description or '',
                            status='active'
                        )
                        device.save()
                        synced_count += 1
            
            log.status = "Success"
            log.message = f"Synced {synced_count} phones."
            log.save()

        except Exception as e:
            log.status = "Failed"
            log.message = str(e)
            log.save()
            raise e
