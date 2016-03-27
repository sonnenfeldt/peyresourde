from de.sonnenfeldt.cbroker.model.hostspecification import HostSpecification

class Request(HostSpecification):

    ha_scale = None
    dr_scale = None
    op_factor = None
    price_limit = None
    image = None
    
    def __init__(self):
        '''
        Constructor
        '''
     
    def __str__(self):
        s = "id: " + str(self.id) + ", host_type_id: " + str(self.host_type_id) + ", region: " + str(self.region_id) + \
        ", cpu: " + str(self.cpu) + ", memory: " + str(self.memory) + ", disk_size: " + str(self.disk_size) + \
        ", disk_type: " + str(self.disk_type_id) + ", ha_scale: " + str(self.ha_scale) + ", dr_scale: " + str(self.dr_scale) + \
        ", op_factor: " + str(self.op_factor) + ", price_limit: " + str(self.price_limit) + \
        ", private: " + str(self.private) + ", optimized: " + str(self.optimized) + ", image: " + str(self.image)
        
        return s
        
