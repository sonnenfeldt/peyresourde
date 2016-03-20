from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker


class CBrokerDB() :
    
    engine = None
    md = None
    session = None
    
    def __init__(self,dburl):
        self.engine = create_engine(dburl)
        self.engine.echo = True
        Session = sessionmaker(self.engine)
        self.session = Session()
        self.md = MetaData(self.engine)
        
    def get_session(self):
        return self.session
        
    def get_host_types(self):
        return Table('hosttype', self.md,autoload=True)

    def get_regions(self):
        return Table('region', self.md, autoload=True)
    
    def get_disk_types(self):
        return Table('disktype', self.md, autoload = True)
    
    def get_availability_zones(self):
        return Table('availabilityzone', self.md, autoload = True)
    
    def get_csps(self):
        return Table('csp', self.md, autoload = True)
    
    def get_host_templates(self):
        return Table('hosttemplate', self.md, autoload = True)
    
    def get_hosts(self):
        return Table('host', self.md, autoload = True)
    
    def get_containers(self):
        return Table('container', self.md, autoload = True)
    
    def get_data_centers(self):
        return Table('datacenter', self.md, autoload = True)
        
    def get_optimization_types(self):
        return Table('optimizationtype',self.md, autoload = True)

    def get_requests(self):
        return Table('request', self.md, autoload = True)
        
    def get_host_domain(self):
        return Table('host_domain', self.md, autoload = True)
    