from de.sonnenfeldt.cbroker.model.host import Host
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig
from sqlalchemy.sql.expression import func

class HostDao():

    host = None

    def __init__(self,host = None):
        if host != None:
            self.host = host
        else:
            self.host = Host()
            
        
    def save(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_hosts()
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
                  host_template_id=self.host.host_template_id,
                  node_uri=self.host.node_uri,
                  node_cluster_uri=self.host.node_cluster_uri)
        
        return oid
        

    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_hosts()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.host.id = res.id
            self.host.host_template_id = res.host_template_id
            self.node_uri = res.node_uri
            self.node_cluster_uri = res.node_cluster_uri
            
        return self.host

    def cleanup(self):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
                
        table = db.get_hosts()        
        d = table.delete()
        d.execute()



h = Host()
h.host_template_id = 2
h.node_uri = 'test1'
h.node_cluster_uri = 'test2'
dao=HostDao(h)

oid = dao.save()
print "oid: ", oid
        
dao2 = HostDao()
r2 = dao2.load(oid)
print r2.toString()   