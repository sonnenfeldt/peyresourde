
class Host():

    id = None
    host_template_id = None
    node_uri = None
    node_cluster_uri = None

    
    def __init__(self):
        '''
        Constructor
        '''
     
    def __str__(self):
        
        s = "id: " + str(self.id) + ", host_template_id: " + str(self.host_template_id) + \
        ", node_uri: " + str(self.node_uri) + ", node_cluster_uri: " + str(self.node_cluster_uri)
        
        return s
        