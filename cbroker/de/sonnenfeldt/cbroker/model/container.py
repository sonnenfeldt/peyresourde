
class Container():

    id = None
    host_id = None
    cpu = None
    memory = None
    disk_size = None
    request_id = None
    container_uri = None

    
    def __init__(self):
        '''
        Constructor
        '''
     
    def __str__(self):
        s = "id: " + str(self.id) + ", host_id: " + str(self.host_id)  + ", cpu: " + str(self.cpu) + \
        ", memory: " + str(self.memory) + ", disk_size: " + str(self.disk_size) + \
        ", request_id: " + str(self.request_id) + ", container_uri: " + self.container_uri
        
        return s
        