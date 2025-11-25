import ldap
from django.contrib.auth.models import User
from ..models import LDAPConfig, SyncLog

class LDAPSync:
    def __init__(self, config: LDAPConfig):
        self.config = config
        self.conn = None

    def connect(self):
        self.conn = ldap.initialize(self.config.server_uri)
        self.conn.simple_bind_s(self.config.bind_dn, self.config.bind_password)

    def unbind(self):
        if self.conn:
            self.conn.unbind_s()

    def sync_users(self):
        log = SyncLog(source="LDAP", status="Running", message="Starting sync...")
        log.save()
        
        try:
            self.connect()
            
            # Search for users
            # Filter example: (&(objectClass=person)(uid=*))
            # We assume a standard filter or could add a field to the model for it.
            # For now, let's assume we want all persons.
            search_filter = "(objectClass=person)"
            
            # Attributes to fetch
            attrs = ['uid', 'cn', 'mail', 'givenName', 'sn']
            
            results = self.conn.search_s(
                self.config.search_base,
                ldap.SCOPE_SUBTREE,
                search_filter,
                attrs
            )
            
            synced_count = 0
            
            for dn, entry in results:
                if not isinstance(entry, dict):
                    continue
                
                # Extract attributes (ldap returns lists of bytes usually)
                def get_attr(k):
                    val = entry.get(k)
                    if val and len(val) > 0:
                        return val[0].decode('utf-8')
                    return ''

                username = get_attr('uid')
                email = get_attr('mail')
                first_name = get_attr('givenName')
                last_name = get_attr('sn')
                
                if not username:
                    continue
                    
                # Check if user exists
                user = User.objects.filter(username=username).first()
                
                if not user:
                    user = User(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        is_active=True
                    )
                    user.set_unusable_password() # External auth usually
                    user.save()
                    synced_count += 1
                else:
                    # Update details
                    changed = False
                    if user.email != email:
                        user.email = email
                        changed = True
                    if user.first_name != first_name:
                        user.first_name = first_name
                        changed = True
                    if user.last_name != last_name:
                        user.last_name = last_name
                        changed = True
                    
                    if changed:
                        user.save()
                        synced_count += 1

            log.status = "Success"
            log.message = f"Synced {synced_count} users."
            log.save()

        except Exception as e:
            log.status = "Failed"
            log.message = str(e)
            log.save()
            raise e
        finally:
            self.unbind()
