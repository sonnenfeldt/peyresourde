from de.sonnenfeldt.cbroker.db.datacenterdao import DataCenterDao
from de.sonnenfeldt.cbroker.model.host import Host
from de.sonnenfeldt.cbroker.db.hostdao import HostDao
from de.sonnenfeldt.cbroker.cb.cloud import CBDockerCloud
from de.sonnenfeldt.cbroker.db.requestdao import RequestDao
from de.sonnenfeldt.cbroker.model.container import Container
from de.sonnenfeldt.cbroker.db.containerdao import ContainerDao


class CBEngine():
    
    hosts = []
    request = None
    docker_cloud = None
    
    is_simulation = False
    
    def __init__(self, ha = None,r = None):
        self.hosts = ha
        self.request = r
        self.docker_cloud = CBDockerCloud()
        
    def __get_region_uri(self,h):
        dao = DataCenterDao()
        region = dao.load(h.data_center_id)
        
        uri = None  
        if region is not None:
            uri = region.data_center_uri
        
        return uri
        
    def __deployHost(self,h):
        region_uri = self.__get_region_uri(h) 
        self.docker_cloud.create_node_cluster(region_uri, h.node_type_uri)
        
        host_id = None
        if (self.docker_cloud.node_cluster_uri is not None) & (self.docker_cloud.node_uri is not None):
            host = Host()
            host.host_template_id = h.id
            host.node_uri = self.docker_cloud.node_uri
            host.node_cluster_uri = self.docker_cloud.node_cluster_uri
            dao = HostDao(host)
            host_id = dao.save()
        
        return host_id
        
    def __deployService(self,h, host_id):
        self.docker_cloud.create_service(self.request.image)
        
        if (self.docker_cloud.service_uri is not None) & (self.docker_cloud.container_uri is not None):
            container = Container()
            container.host_id = host_id
            container.cpu = self.request.cpu
            container.memory = self.request.memory
            container.disk_size = self.request.disk_size
            container.request_id = self.request.id
            container.service_uri = self.docker_cloud.service_uri
            container.container_uri = self.docker_cloud.container_uri
            dao = ContainerDao(container)
            container_id = dao.save()
            
        return container_id
        
    def deploy(self):
        
        if self.is_simulation is not True:             
            dao = RequestDao(self.request)
            request_id = dao.save()
            self.request = dao.load(request_id)
            
            for h in self.hosts:
                if h.host_id is None:
                    host_id = self.__deployHost(h)
                    self.__deployService(h, host_id)
                else:
                    hostDao = HostDao()
                    host = hostDao.load(h.host_id)
                    self.docker_cloud.node_cluster_uri = host.node_cluster_uri
                    self.__deployService(h, h.host_id)
                    

    def terminate(self, container_id):
        dao = ContainerDao()
        container = dao.load(container_id)
        host_id = container.host_id
        self.docker_cloud.terminate_service(container.service_uri)
        dao.delete(container_id)
            
        if dao.is_empty(host_id):
            dao = HostDao()
            h = dao.load(host_id)
            self.docker_cloud.terminate_node_cluster(h.node_cluster_uri)
            dao.delete(host_id)
        
     
        
        
        