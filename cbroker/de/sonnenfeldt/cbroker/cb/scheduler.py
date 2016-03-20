from de.sonnenfeldt.cbroker.cp.model import CBBrokerModel
from de.sonnenfeldt.cbroker.cp.variables import CBrokerVariables
from de.sonnenfeldt.cbroker.cp.solver import CBrokerSolver
from de.sonnenfeldt.cbroker.model.hostdomain import HostDomain
from de.sonnenfeldt.cbroker.db.hostdomaindao import HostDomainDao
from de.sonnenfeldt.cbroker.model.request import Request
from Numberjack import Minimise 
from Numberjack import SAT

class Scheduler():
    
    r = None
    hosts = []
    
    def __init__(self, request):
        self.r = request

    def __read(self,v):
        hd = HostDomain()
        hd.provider_id = v.provider.get_value()
        hd.host_type_id = v.host_type.get_value()
        hd.region_id = v.region.get_value()
        hd.data_center_id = v.data_center.get_value()
        hd.az_index = v.az.get_value()
        hd.cpu = v.cpu.get_value()
        hd.memory = v.memory.get_value()
        hd.disk_size = v.disk_size.get_value()
        hd.disk_type_id = v.disk_type.get_value()
        hd.private = v.private.get_value()
        hd.optimized = v.optimized.get_value()
        hd.cost = v.cost.get_value()
        
        return hd

    def __single_host(self):
        v = CBrokerVariables()
        m = CBBrokerModel(self.r)
            
        m.addHosts(v)           
        m.addRequest()
        m.addObjective(Minimise(v.cost))
        
        s = CBrokerSolver(m)
 
        i = 0
        if s.solve():
            i+=1
            h = self.__read(v)
                
            dao = HostDomainDao()
            h = dao.load_using_host(h)

            while s.getNextSolution() == SAT:
                i+= 1
                
            print "Number Solutions: ", i
            print 'Nodes:', s.s.getNodes(), ' Time:', s.s.getTime()
        else:
            print "No solution"        
            
        return h
    
    def __multiple_hosts(self):
        '''
        '''
    
    def process(self):

        if (self.r.dr_scale == 1) & (self.r.ha_scale == 1):
            # TODO: check for running host with free capacity
            # invoke dao and get the result set, if result.rowcount > 0, then ise it
            h = self.__single_host()
            
            self.hosts.append(h)
        
            #else:
            
            # m.addAntiCollocation(v1,v2)
            
        return self.hosts           
        
    
r = Request()
r.host_type_id = 0
r.region_id = 2
r.cpu = 1
r.memory = 2
r.disk_size = 3
r.disk_type_id = 0
r.ha_scale = 1
r.dr_scale = 1
r.op_factor = 4
r.price_limit = 10000
r.optimized = 0
r.private = 0
r.service_uri = 'test'

s = Scheduler(r)
hd = s.process()
print hd

