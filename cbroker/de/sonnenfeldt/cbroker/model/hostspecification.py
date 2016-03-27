from de.sonnenfeldt.cbroker.model.resource import Resource

class HostSpecification(Resource):

    host_type_id = None
    region_id = None
    disk_type_id = None
    private = None
    optimized = None
    
    def __init__(self):
        '''
        Constructor
        '''

        