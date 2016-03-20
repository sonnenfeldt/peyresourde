from de.sonnenfeldt.cbroker.db.cbrokerdb import CBrokerDB

class DBConfig():
    
    url = 'mysql://root:Husa4vik!@cbroker-1.493210ed.cont.dockerapp.io:32768/cbroker'
    db = None
    
    def __init__(self):
        self.db = CBrokerDB(self.url)
        
    def get_db(self):
        return self.db