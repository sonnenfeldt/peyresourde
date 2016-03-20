
class Request():

    id = None
    host_type_id = None
    region_id = None
    cpu = None
    memory = None
    disk_size = None
    disk_type_id = None
    ha_scale = None
    dr_scale = None
    op_factor = None
    price_limit = None
    private = None
    optimized = None
    service_uri = None
    
    def __init__(self):
        '''
        Constructor
        '''
     
    def toString(self):
        s = "id: " + str(self.id) + ", host_type_id: " + str(self.host_type_id) + ", region: " + str(self.region_id) + \
        ", cpu: " + str(self.cpu) + ", memory: " + str(self.memory) + ", disk_size: " + str(self.disk_size) + \
        ", disk_type: " + str(self.disk_type_id) + ", ha_scale: " + str(self.ha_scale) + ", dr_scale: " + str(self.dr_scale) + \
        ", op_factor: " + str(self.op_factor) + ", price_limit: " + str(self.price_limit) + \
        ", private: " + str(self.private) + ", optimized: " + str(self.optimized) + ", service_uri: " + self.service_uri
        
        return s
        
