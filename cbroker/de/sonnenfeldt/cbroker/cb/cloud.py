import dockercloud
import time
import uuid
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('dockercloud.properties')
dockercloud.user = config.get('Credentials', 'dockercloud.user')
dockercloud.apikey = config.get('Credentials','dockercloud.apikey')

class CBDockerCloud():
        
    node_cluster_uri = None
    node_uri = None
    cluster_name = None
    service_name = None
    service_uri = None
    container_uri = None
    
    MAX_WAIT_TIME = 900
    API_REGION_PREFIX='/api/infra/v1/region/'
    API_NODETYPE_PREFIX='/api/infra/v1/nodetype/'
    API_NODECLUSTER_PREFIX='/api/infra/v1/nodecluster/'
    API_NODE_PREFIX='/api/infra/v1/node/'
    API_SERVICE_PREFIX='/api/app/v1/service/'
    API_CONTAINER_PREFIX='/api/app/v1/container/'
    API_SUFFIX='/'
    
    STATE_DEPLOYED='Deployed'
    STATE_RUNNING='Running'
    STATE_TERMINATED='Terminated'
    
    TAG_NODECLUSTER_NAME='nodecluster-name='
    
    CLUSTER_NAME_PREFIX='cbcluster'
    SERVICE_NAME_PREFIX='service'
        
    def __init__(self,node_cluster_uri=None,node_uri=None):
        self.node_cluster_uri = node_cluster_uri
        self.node_uri = node_uri

        
    def __cut(self,s,prefix,suffix):
        print "__cut: ", s, prefix, suffix
        if s.startswith(prefix):
            s = s[len(prefix):]
        if s.endswith(suffix):
            s = s[:-len(suffix)]
        print "__cut: ", s
        return s
            
        
    def create_node_cluster(self,region_uri,node_type_uri):


        region = dockercloud.Region.fetch(self.__cut(region_uri,self.API_REGION_PREFIX,self.API_SUFFIX))
        print "region: ", region.name
        node_type = dockercloud.NodeType.fetch(self.__cut(node_type_uri,self.API_NODETYPE_PREFIX,self.API_SUFFIX))
        print "node_type: ", node_type.name
        
        self.cluster_name = self.CLUSTER_NAME_PREFIX + str(uuid.uuid4())[:8]
        nodecluster = dockercloud.NodeCluster.create(name=self.cluster_name, node_type=node_type, region=region, target_num_nodes = 1)
        nodecluster.save()
        nodecluster.deploy()
        
        self.node_cluster_uri = nodecluster.resource_uri
                
        t = 0
        while (nodecluster.state != self.STATE_DEPLOYED) & (t < self.MAX_WAIT_TIME):
            print "Waiting for cluster to be deployed."
            time.sleep(10)
            t+=10
            nodecluster = dockercloud.NodeCluster.fetch(self.__cut(self.node_cluster_uri,self.API_NODECLUSTER_PREFIX,self.API_SUFFIX))
            
        node = None
        for n in nodecluster.nodes:
            node = dockercloud.Node.fetch(self.__cut(n,self.API_NODE_PREFIX,self.API_SUFFIX))

        if node is not None:
            self.node_uri = node.resource_uri
        
            t = 0
            while (node.state != self.STATE_DEPLOYED) & (t < self.MAX_WAIT_TIME):
                print "Waiting for node to be deployed."
                time.sleep(10)
                t+=10
                node = dockercloud.Node.fetch(self.__cut(self.node_uri,self.API_NODE_PREFIX,self.API_SUFFIX))

        print "self.node_cluster_uri: ", self.node_cluster_uri
        print "self.node_uri: ", self.node_uri
        
        # store nodecluster.uuid
        # store cluster name
        # generate cbcluster name using id of the host to created - add necessary columns to nodecluster
        
    def create_service(self,image):
        
        nodecluster = dockercloud.NodeCluster.fetch(self.__cut(self.node_cluster_uri,self.API_NODECLUSTER_PREFIX,self.API_SUFFIX))
        
        self.cluster_name = nodecluster.name
        self.service_name = self.SERVICE_NAME_PREFIX + str(uuid.uuid4())[:8]
        
        tag = self.TAG_NODECLUSTER_NAME + self.cluster_name
        
        service = dockercloud.Service.create(image=image, name=self.service_name, target_num_containers=1, tags=[tag])
        service.save()
        service.start()

        self.service_uri = service.resource_uri

        t = 0
        while (service.state != self.STATE_RUNNING)  & (t < self.MAX_WAIT_TIME):
            print "Waiting for service to be running."
            time.sleep(10)
            t+=10
            service = dockercloud.Service.fetch(self.__cut(self.service_uri,self.API_SERVICE_PREFIX,self.API_SUFFIX))
            
        container = None
        for c in service.containers:
            container = dockercloud.Container.fetch(self.__cut(c,self.API_CONTAINER_PREFIX,self.API_SUFFIX))
      
        if container is not None:
            self.container_uri = container.resource_uri 
            
            t = 0 
            while (container.state != self.STATE_RUNNING) & (t < self.MAX_WAIT_TIME):
                print "Waiting for container to be running."
                time.sleep(10)
                t+=10
                container = dockercloud.Container.fetch(self.__cut(c,self.API_CONTAINER_PREFIX,self.API_SUFFIX))
        
        print "self.service_uri: ", self.service_uri
        print "self.container_uri: ", self.container_uri
        
    def terminate_service(self,service_uri):
        service = dockercloud.Service.fetch(self.__cut(service_uri,self.API_SERVICE_PREFIX,self.API_SUFFIX))
    
        service.delete()
        t = 0
        while (service.state != self.STATE_TERMINATED)  & (t < self.MAX_WAIT_TIME):
            print "Waiting for service to be terminated."
            time.sleep(10)
            t+=10
            service = dockercloud.Service.fetch(self.__cut(service_uri,self.API_SERVICE_PREFIX,self.API_SUFFIX))    
    
    
    def terminate_node_cluster(self, node_cluster_uri):
        nodecluster = dockercloud.NodeCluster.fetch(self.__cut(node_cluster_uri,self.API_NODECLUSTER_PREFIX,self.API_SUFFIX))
        
        nodecluster.delete()
 
        t = 0
        while (nodecluster.state != self.STATE_TERMINATED) & (t < self.MAX_WAIT_TIME):
            print "Waiting for cluster to be terminated."
            time.sleep(10)
            t+=10
            nodecluster = dockercloud.NodeCluster.fetch(self.__cut(node_cluster_uri,self.API_NODECLUSTER_PREFIX,self.API_SUFFIX))       
