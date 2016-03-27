from de.sonnenfeldt.cbroker.cp.model import CBModel
from de.sonnenfeldt.cbroker.cp.variables import CBVariables
from de.sonnenfeldt.cbroker.cp.solver import CBSolver
from de.sonnenfeldt.cbroker.model.hostdomain import HostDomainMember
from de.sonnenfeldt.cbroker.db.hostdomaindao import HostDomainDao
from de.sonnenfeldt.cbroker.model.request import Request
from Numberjack import Minimise 
from Numberjack import SAT

class CBPlanner():
    
    r = None
    hosts = []
    
    def __init__(self, request):
        self.r = request

    def __read(self,v):
        hd = HostDomainMember()
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
        v = CBVariables()
        m = CBModel(self.r)


        m.addObjective(Minimise(v.cost))
        m.addRequest(v)            
        m.addHosts(v)           

        s = CBSolver(m)
 
        h = None
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


        m = CBModel(self.r)

        va = [[None for y in range(self.r.ha_scale)] for x in range(self.r.dr_scale)]
           
        obj = None   
        print 'obj:', obj        
        
        for x in range(self.r.dr_scale):
            print 'obj before 2nd for:', obj        
            for y in range(self.r.ha_scale):
                v = CBVariables()
                m.addRequest(v)            
                m.addHosts(v)
 
                print 'obj before if:', obj               
                if obj is None:
                    print '1',x,y
                    obj = v.cost
                else:
                    print '2',x,y
                    obj = obj + v.cost
                    
                print 'obj:', obj                                
                va[x][y] = v
        
        m.addAnticollcation(va)
        
        m.addObjective(Minimise(obj))
    
        #print m.m
    
        s = CBSolver(m)
 
        ha = []
        i = 0
        if s.solve():
            i+=1
            dao = HostDomainDao()

            for x in range(self.r.dr_scale):
                for y in range(self.r.ha_scale):
                    h = self.__read(va[x][y])
                    h = dao.load_using_host(h)
                    ha.append(h)
            
            while s.getNextSolution() == SAT:
                i+= 1
                
            print "Number Solutions: ", i
            print 'Nodes:', s.s.getNodes(), ' Time:', s.s.getTime()
        else:
            print "No solution"        
        
        for h in ha:
            print h        
            
        return ha
        
    
    def process(self):

        # implement different means of HA - across different DCs in the same regions
   
        self.hosts = self.__multiple_hosts()
               
        return self.hosts           
        