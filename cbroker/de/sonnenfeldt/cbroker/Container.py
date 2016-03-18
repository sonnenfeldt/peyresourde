'''
Created on 8 Dec 2015

@author: rudi
'''

class Container():
    '''
    classdocs
    '''
    HOST_TYPES = ["virtual", "hw"]
    ENVIRONMENT_TYPES = ["dev/test","prod"]
    IS_OPTIMIZED = ["yes", "no"]
    DISK_TYPES = ["HDD", "SDD"]
    OS_TYPES = ["Linux", "Windows"]
    REGIONS = ["Germany","France","Ireland","Australia","Brazil","Canada","China","Great Britain","India","Japan",
               "Mexico","Netherlands","Singapore","California,U.S.","Illinois,U.S.","Texas,U.S.","Iowa,U.S",
               "New York,U.S","Oregon,U.S.","Washington,U.S.","Virgina,U.S."]
    PROVIDERS= ["Azure", "AWS", "SoftLayer", "Digital Ocean"] 

    regions = []

    def __init__(self):
        '''
        Constructor
        '''
        
    def assign_host_type(self, host_type):
        self.host_type = host_type
        
    def get_host_type(self):
        return self.host
        
    def assign_environment_type(self, env_type):
        self.environment_type = env_type
        
    def get_environment_type(self):
        return self.environment_type    
        
    def assign_regions(self, region):
        self.regions.append(region)
        
    def get_regions(self):
        return self.regions
        
    def assign_disk_type(self, disk_type):
        self.disk_type = disk_type
        
    def get_disk_type(self):
        return self.disk_type
        
    def assign_compute_optimized(self, compute_optimized):
        self.compute_optimized = compute_optimized
        
    def get_compute_optimized(self):
        return self.compute_optimized    
        
    def assign_memory_optimized(self, memory_optimized):
        self.memory_optimized = memory_optimized
        
    def get_memory_optimized(self):
        return self.memory_optimized 
        
    def assign_storage_optimized(self, storage_optimized):
        self.storage_optimized = storage_optimized
        
    def get_storage_optimized(self):
        return self.storage_optimized    
        
    def assign_cpus(self, cpus):
        self.cpus = cpus
        
    def get_cpus(self):
        return self.cpus    
        
    def assign_memory(self, memory):
        self.memory = memory
        
    def get_memory(self):
        return self.memory
        
    def assign_disk_size(self, disk_size):
        self.disk_size = disk_size
        
    def get_disk_size(self):
        return self.disk_size    
        
    def assign_ha_scale(self, ha_scale):
        self.ha_scale = ha_scale
        
    def get_ha_scale(self): 
        return self.ha_scale   
        
    def assign_dr_scale(self, dr_scale):
        self.dr_scale = dr_scale
        
    def get_dr_scale(self):
        return self.dr_scale    
        
    def assign_price_limit(self, price_limit):
        self.price_limit = price_limit;
        
    def get_price_limit(self):
        return self.price_limit    