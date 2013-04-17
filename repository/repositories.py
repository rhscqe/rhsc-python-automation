from helpers.waiter import Waiter
from factories.param_factory import ParamFactory

class DatacenterRepository:
    @classmethod
    def create(cls,api,params=ParamFactory().create_datacenter()):
        return api.datacenters.add(params) 

class ClusterRepository:
    @classmethod
    def create(cls,api,params=ParamFactory().create_cluster()):
        return api.clusters.add(params)

class HostRepository:
    @classmethod
    def create(cls,api,params):
        return api.hosts.add(params) 

    @classmethod 
    def show(cls,api,host):
        return api.hosts.get(id=host.id)

    @classmethod 
    def refresh(cls,api,host):
        return cls.show(api,host)

    @classmethod 
    def stop_and_wait_for_status_maintanence(cls,api,host):
        host.deactivate()
        Waiter.waitUntil(lambda : Waiter.host_is_maintanence(api,host), 200)

class VolumeRepository:
    @classmethod
    def create(cls,cluster,params):
        return cluster.glustervolumes.add(params)

