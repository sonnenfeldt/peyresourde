from Numberjack import Model
from de.sonnenfeldt.cbroker.db.hostdomaindao import HostDomainDao
from de.sonnenfeldt.cbroker.cp.variables import CBVariables
from de.sonnenfeldt.cbroker.model.request import Request


class CBModel():
    
    m = None
    r = None
  #  s = None
    
    az_supported = False
    
    def __init__(self, request):
        self.m = Model()
        self.r = request
        print 'request: ', self.r
        
    def __and(self, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12):
        expr = (b1 & b2 & b3 & b4 & b5 & b6 & b7 & b8 & b9 & b10 & b11 & b12)
        return expr

    def __or(self, b1, b2):
        expr = (b1 | b2)
        return expr        
        
    def addHosts(self, v):
        
        dao = HostDomainDao()
        result = dao.load_using_request(self.r)

        print 'result.rowcount: ', result.rowcount

        expr = False        
        for res in result:
            expr = self.__or(expr,self.__and(v.provider == int(res.provider_id), 
                            v.host_type == int(res.host_type_id), 
                            v.region == int(res.region_id), 
                            v.data_center == int(res.data_center_id), 
                            v.az == int(res.az_index), 
                            v.cpu == int(res.cpu), 
                            v.memory == int(res.memory), 
                            v.disk_size == int(res.disk_size), 
                            v.disk_type == int(res.disk_type_id), 
                            v.private == int(res.private), 
                            v.optimized == int(res.optimized), 
                            v.cost == int(res.cost)))
          
        self.m.add(expr)
        #print self.m


    def addRequest(self, v):
        
        print "request: ", self.r
        
        if (self.r.host_type_id > 0):
            self.m.add(v.host_type == int(self.r.host_type_id))
            
        if (self.r.region_id > 0):    
            self.m.add(v.region == int(self.r.region_id))
   
        self.m.add(v.cpu >= int(self.r.cpu * self.r.op_factor))
   
        self.m.add(v.memory >= int(self.r.memory * self.r.op_factor))
        self.m.add(v.disk_size >= int(self.r.disk_size * self.r.op_factor))
        
        if (self.r.disk_type_id > 0):    
            self.m.add(v.disk_type == int(self.r.disk_type_id))        

        if (self.r.price_limit > 0):    
            self.m.add(v.cost <= int(self.r.price_limit))  
           
        if (self.r.private > 0):    
            self.m.add(v.private == int(self.r.private))
            
        if (self.r.optimized > 0):
            self.m.add(v.optimized == int(self.r.optimized))
        
        #print self.m

        
    def addObjective(self, expr):
        self.m.add(expr)

    def addAnticollcation(self,va):
        # add ha anti-collocation constraints
        for x in range(self.r.dr_scale):
            for y_1 in range(self.r.ha_scale):
                for y_2 in range(self.r.ha_scale):
                    if y_1!=y_2:
                        self.m.add( ((va[x][y_1].az != va[x][y_2].az) &  (va[x][y_1].data_center == va[x][y_2].data_center) & self.az_supported)  |
                                    ((va[x][y_1].data_center != va[x][y_2].data_center) & (va[x][y_1].region == va[x][y_2].region))
                                     )
                

        # add different region for DR
        for x_1 in range(self.r.dr_scale):
            for x_2 in range(self.r.dr_scale):
                if x_1 != x_2:
                    for y_1 in range(self.r.ha_scale):
                        for y_2 in range(self.r.ha_scale):
                            self.m.add(va[x_1][y_1].region != va[x_2][y_2].region) 
    
r = Request()
r.host_type_id = 0
r.region_id = 0
r.cpu = 1
r.memory = 2
r.disk_size = 3
r.disk_type_id = 0
r.ha_scale = 1
r.dr_scale = 1
r.op_factor = 1
r.price_limit = 10000
r.optimized = 0
r.private = 0
r.service_uri = 'test'

v = CBVariables()
m = CBModel(r)
m.addHosts(v)