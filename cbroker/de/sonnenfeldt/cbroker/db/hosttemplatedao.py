from de.sonnenfeldt.cbroker.model.hosttemplate import HostTemplate
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig
from sqlalchemy.sql.expression import func

class HostTemplateDao():

    host_template = None

    def __init__(self,host_template = None):
        if host_template != None:
            self.host_template = host_template
        else:
            self.host_template = HostTemplate()
                    

    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_host_templates()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.host_template.id = res.id
            self.host_template.name = res.name
            self.host_template.provider_id = res.provider_id
            self.host_template.host_type_id = res.host_type_id
            self.host_template.region_id = res.region_id
            self.host_template.data_center_id = res.data_center_id
            self.host_template.az_index = res.az_index
            self.host_template.cpu = res.cpu
            self.host_template.memory = res.memory
            self.host_template.disk_size = res.disk_size
            self.host_template.disk_type_id = res.disk_type_id
            self.host_template.private = res.private
            self.host_template.optimized = res.optimized            
            self.host_template.cost = res.cost
            self.host_template.node_type_uri = res.node_type_uri
            
        return self.host_template
