from Numberjack import Model
from de.sonnenfeldt.cbroker.db.hostdomaindao import HostDomainDao
from de.sonnenfeldt.cbroker.cp.variables import CBrokerVariables
from de.sonnenfeldt.cbroker.model.request import Request


class CBBrokerModel():
    
    m = None
    r = None
    s = None
    
    def __init__(self, request):
        self.m = Model()
        self.r = request
        
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


    def addRequest(self):
        
        if (r.host_type_id > 0):
            self.m.add(v.host_type == int(r.host_type_id))
            
        if (r.region_id > 0):    
            self.m.add(v.region == r.region_id)
   
        self.m.add(v.cpu >= int(r.cpu * r.op_factor))
   
        self.m.add(v.memory >= int(r.memory * r.op_factor))
        self.m.add(v.disk_size >= int(r.disk_size * r.op_factor))
        
        if (r.disk_type_id > 0):    
            self.m.add(v.disk_type == int(r.disk_type_id))        

        if (r.price_limit > 0):    
            self.m.add(v.cost <= int(r.price_limit))  
            
        self.m.add(v.private == int(r.private))
        self.m.add(v.optimized == int(r.optimized))

        
    def addObjective(self, expr):
        self.m.add(expr)

 


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

v = CBrokerVariables()
m = CBBrokerModel(r)
m.addHosts(v)