from de.sonnenfeldt.cbroker.cb.planner import CBPlanner
from de.sonnenfeldt.cbroker.cb.engine import CBEngine
from de.sonnenfeldt.cbroker.model.request import Request
from de.sonnenfeldt.cbroker.db.containerdao import ContainerDao

import time

class CBroker():
    
    request = None
    
    def __init__(self, r = None):
        if r is not None:
            self.request = r
        else:
            self.request = Request()
    
    def process(self):
        p = CBPlanner(self.request)
        hosts = p.process()       
        e = CBEngine(hosts,self.request)
        e.deploy()
                
    def terminate(self, container_id):
        e = CBEngine()
        e.terminate(container_id)
        
    def terminate_all(self):
        dao = ContainerDao()
        cons = dao.load_all()
        for c in cons:
            self.terminate(c.id)

if __name__ == "__main__":
    r = Request()
    r.host_type_id = 0
    r.region_id = 0
    r.cpu = 1
    r.memory = 2
    r.disk_size = 5
    r.disk_type_id = 0
    r.ha_scale = 1
    r.dr_scale = 1
    r.op_factor = 1 
    r.price_limit = 1000
    r.optimized = 0
    r.private = 0
    r.image = "appcontainers/wordpress:latest"
    
    broker = CBroker(r)
    broker.process()
    
#    time.sleep(600)
    
#    broker = CBroker()
#    broker.terminate_all()  