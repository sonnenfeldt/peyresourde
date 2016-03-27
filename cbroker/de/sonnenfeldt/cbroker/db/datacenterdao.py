from de.sonnenfeldt.cbroker.model.datacenter import DataCenter
from de.sonnenfeldt.cbroker.db.dbconfig import DBConfig
from sqlalchemy.sql.expression import func

class DataCenterDao():

    data_center = None

    def __init__(self):
        self.data_center = DataCenter()
            
            
    def load(self,oid):
        dbconfig = DBConfig()
        db = dbconfig.get_db()
        
        table = db.get_data_centers()
        s = table.select(table.c.id == oid)
        result = s.execute()

        for res in result:
            self.data_center.id = res.id
            self.data_center.name = res.name
            self.data_center.region_id = res.region_id
            self.data_center.data_center_uri = res.data_center_uri
            
        return self.data_center
