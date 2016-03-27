from de.sonnenfeldt.cbroker.db.cbrokerdb import CBrokerDB
import ConfigParser

class DBConfig():
    
    
    config = ConfigParser.RawConfigParser()
    config.read('cbrokerdb.properties')
    
    user = config.get('MySQL', 'database.user')
    password = config.get('MySQL','database.password')
    hostname = config.get('MySQL','database.hostname')
    port = config.get('MySQL','database.port')

    url = 'mysql://' + user + ':' + password + '@' + hostname + ':' + port + '/cbroker'
    
    db = None
    
    def __init__(self):
        self.db = CBrokerDB(self.url)
        
    def get_db(self):
        return self.db