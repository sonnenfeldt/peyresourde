from de.sonnenfeldt.cbroker.model.container import Container
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig
from sqlalchemy.sql.expression import func

class ContainerDao():

    container = None

    def __init__(self,container = None):
        if container != None:
            self.container = container
        else:
            self.container = Container()
            
        
    def save(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_containers()
        session = db.get_session()
        
        
        qry = session.query(func.max(table.c.id).label("max_id"))
        res = qry.one()
        oid = res.max_id
        
        print "oid: ", oid
        
        if oid > -1:
            oid = oid + 1
        else:
            oid = 1
        
        i = table.insert()
        i.execute(id=oid,
                  host_id=self.container.host_id,
                  cpu=self.container.cpu,
                  memory=self.container.memory,
                  disk_size=self.container.disk_size,
                  request_id=self.container.request_id,
                  service_uri=self.container.service_uri,
                  container_uri=self.container.container_uri)
        
        return oid
        

    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_containers()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.container.id = res.id
            self.container.host_id = res.host_id
            self.container.cpu = res.cpu
            self.container.memory = res.memory
            self.container.disk_size = res.disk_size
            self.container.request_id = res.request_id
            self.container.service_uri = res.service_uri
            self.container.container_uri = res.container_uri
            
        return self.container


    def load_all(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_containers()     
                    
        s = table.select()
        result = s.execute()
        
        print 'result.rowcount: ', result.rowcount
                
        return result
       
    def delete(self, oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_containers()
        s = table.delete(table.c.id == oid)
        s.execute()
    
    def is_empty(self, host_id):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_containers() 
        s = table.select(table.c.host_id == host_id)
        result = s.execute()
        
        print "is_empty:", (result.rowcount == 0)
        return (result.rowcount == 0)
                   
    
    def cleanup(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
                
        table = db.get_containers()        
        d = table.delete()
        d.execute()

