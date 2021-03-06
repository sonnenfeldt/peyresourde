from de.sonnenfeldt.cbroker.model.hosttemplate import HostTemplate

class HostDomainMember(HostTemplate):

 
    host_id = None
    
    def __init__(self):
        '''
        Constructor
        '''
     
    def __str__(self):
        s = "id: " + str(self.id) + ", host_id: " + str(self.host_id) + ", provider_id: " + str(self.provider_id) + \
        ", host_type_id: " + str(self.host_type_id) + ", region_id: " + str(self.region_id) + \
        ", data_center_id: " + str(self.data_center_id) + ", az_index: " + str(self.az_index) + \
        ", cpu: " + str(self.cpu) + ", memory: " + str(self.memory) + ", disk_size: " + str(self.disk_size) + \
        ", disk_type_id: " + str(self.disk_type_id) + ", private: " + str(self.private) + \
        ", optimized: " + str(self.optimized) + ", cost: " + str(self.cost) + \
        ", node_type-uri: " + str(self.node_type_uri)
        
        return s
        