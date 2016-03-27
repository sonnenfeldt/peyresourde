from de.sonnenfeldt.cbroker.model.request import Request
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig
from sqlalchemy.sql.expression import func

class RequestDao():

    request = None

    def __init__(self,request = None):
        if request is not None:
            self.request = request
        else:
            self.request = Request()
            
        
    def save(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_requests()
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
                  host_type_id=self.request.host_type_id,
                  region_id=self.request.region_id,
                  cpu=self.request.cpu,
                  memory=self.request.memory,
                  disk_size=self.request.disk_size,
                  disk_type_id=self.request.disk_type_id,
                  ha_scale=self.request.ha_scale,
                  dr_scale=self.request.dr_scale,
                  op_factor=self.request.op_factor,
                  price_limit=self.request.price_limit,
                  private=self.request.private,
                  optimized=self.request.optimized,
                  image=self.request.image)
        
        return oid
        

    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_requests()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.request.id = res.id
            self.request.host_type_id = res.host_type_id
            self.request.region_id = res.region_id
            self.request.cpu = res.cpu
            self.request.memory = res.memory
            self.request.disk_size = res.disk_size
            self.request.disk_type_id = res.disk_type_id
            self.request.ha_scale = res.ha_scale
            self.request.dr_scale = res.dr_scale
            self.request.op_factor = res.op_factor
            self.request.price_limit = res.price_limit
            self.request.optimized = res.optimized
            self.request.private = res.private
            self.request.image = res.image
            
        return self.request

    def cleanup(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
                
        table = db.get_requests()        
        d = table.delete()
        d.execute()
