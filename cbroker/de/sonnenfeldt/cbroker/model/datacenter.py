
class DataCenter():

    id = None
    name = None
    region_id = None
    data_center_uri = None

    
    def __init__(self):
        '''
        Constructor
        '''
     
    def __str__(self):
        
        s = "id: " + str(self.id) + ", name: " + str(self.name) + \
        ", region_id: " + str(self.region_id) + ", data_center_uri: " + str(self.data_center_uri)
        
        return s