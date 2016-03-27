from de.sonnenfeldt.cbroker.model.hostdomain import HostDomainMember
from de.sonnenfeldt.cbroker.model.request import Request
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig

class HostDomainDao():

    host_domain = None

    def __init__(self,host_domain = None):
        if host_domain != None:
            self.host_domain = host_domain
        else:
            self.host_domain = HostDomainMember()
                    

    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_host_domain()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.host_domain.id = res.id
            self.host_domain.name = res.name
            self.host_domain.provider_id = res.provider_id
            self.host_domain.host_type_id = res.host_type_id
            self.host_domain.region_id = res.region_id
            self.host_domain.data_center_id = res.data_center_id
            self.host_domain.az_index = res.az_index
            self.host_domain.cpu = res.cpu
            self.host_domain.memory = res.memory
            self.host_domain.disk_size = res.disk_size
            self.host_domain.disk_type_id = res.disk_type_id
            self.host_domain.private = res.private
            self.host_domain.optimized = res.optimized            
            self.host_domain.cost = res.cost
            self.host_domain.node_type_uri = res.node_type_uri
            
        return self.host_domain


    def load_using_request(self, r):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_host_domain()        
        
        expr = ((table.c.cpu >= (r.cpu * r.op_factor)) | ((table.c.host_id != None) & (table.c.cpu  >= r.cpu)) )
        expr = expr & ((table.c.memory >= (r.memory * r.op_factor)) | ((table.c.host_id != None) & (table.c.memory >= r.memory)))
        expr = expr & ((table.c.disk_size >= (r.disk_size * r.op_factor)) | ((table.c.host_id != None) & (table.c.disk_size >= r.disk_size)))

        
        if (r.host_type_id > 0):
            expr = expr & (table.c.host_type_id == r.host_type_id)
            
        if (r.region_id > 0):    
            expr = expr & (table.c.region_id == r.region_id)
        
        if (r.disk_type_id > 0):    
            expr = expr & (table.c.disk_type_id == r.disk_type_id)
            
        if (r.price_limit > 0):    
            expr = expr & ((table.c.cost <= r.price_limit) )
            
        if (r.private > 0):
            expr = expr & (table.c.private == r.private)
        
        if (r.optimized > 0):
            expr = expr & (table.c.optimized == r.optimized)            
                        
        s = table.select(expr)
        result = s.execute()
        
        return result
        
    def load_using_host(self, hd):
        
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_host_domain()        
        
        expr = (table.c.provider_id == hd.provider_id) & (table.c.host_type_id == hd.host_type_id)
        expr = expr & (table.c.region_id == hd.region_id) & (table.c.data_center_id == hd.data_center_id)
        expr = expr & (table.c.az_index == hd.az_index) & (table.c.cpu == hd.cpu) 
        expr = expr & (table.c.memory == hd.memory) & (table.c.disk_size == hd.disk_size)
        expr = expr & (table.c.disk_type_id == hd.disk_type_id) & (table.c.private == hd.private)
        expr = expr & (table.c.optimized == hd.optimized) & (table.c.cost == hd.cost)  
                    
        s = table.select(expr)
        result = s.execute()
        
        print 'result.rowcount: ', result.rowcount
        
        for res in result:
            hd.id = res.id
            hd.host_id = res.host_id
            hd.node_type_uri = res.node_type_uri
        
        return hd
