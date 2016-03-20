from Numberjack import Variable

class CBrokerVariables():
   
    MAX_PROVIDERS = 5
    MAX_HOST_TYPES = 2
    MAX_REGIONS = 22
    MAX_DATA_CENTERS = 52    
    MAX_AZ = 5
    MAX_CPU = 40
    MAX_MEMORY = 448
    MAX_DISK_SIZES = 48000
    MAX_DISK_TYPES = 2
    MAX_PRIVATE = 1
    MAX_OPTIMIZED = 5
    MAX_COST = 99999

    provider = None
    host_type = None
    region = None
    data_center = None
    az = None
    cpu = None
    memory = None
    disk_size = None
    disk_type = None
    private = None
    optimized = None
    cost = None
        
    def __init__(self):
        # initialize variables
        self.provider = Variable(1,self.MAX_PROVIDERS, "provider")
        self.host_type = Variable(1, self.MAX_HOST_TYPES, "host_type")
        self.region = Variable(1,self.MAX_REGIONS,"region")
        self.data_center = Variable(1,self.MAX_DATA_CENTERS,"data_center")
        self.az = Variable(1,self.MAX_AZ,"az")
        self.cpu = Variable(1,self.MAX_CPU,"cpu")
        self.memory = Variable(1,self.MAX_MEMORY,"memory")
        self.disk_size = Variable(1,self.MAX_DISK_SIZES,"disk_size")
        self.disk_type = Variable(1,self.MAX_DISK_TYPES,"disk_type")   
        self.private = Variable(0,self.MAX_PRIVATE,"private")
        self.optimized = Variable(0,self.MAX_OPTIMIZED,"optimized")
        self.cost = Variable(1,self.MAX_COST,"cost")  

