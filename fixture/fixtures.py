from repository.repositories import DatacenterRepository
from repository.repositories import ClusterRepository
from repository.repositories import HostRepository
from repository.repositories import VolumeRepository
from factories.param_factory import ParamFactory
from helpers.waiter import Waiter


class ReturnAll:
    def __init__(self,datacenter,cluster,host):
        self.datacenter=datacenter
        self.cluster=cluster
        self.host=host
    

class FixtureFactory:
    def __init__(self,api):
        self.api = api

    def create_datacenter(self,datacenter=ParamFactory().create_datacenter()):
        return DatacenterRepository(self.api).show(datacenter) or DatacenterRepository(self.api).create(datacenter)

    def create_cluster(self,params=ParamFactory().create_cluster()):
        return ClusterRepository(self.api).show(params) or ClusterRepository(self.api).create(params)

    def create_host(self, params):
        return self.api.hosts.get(params.get_name()) or HostRepository(self.api).create(params)

    def create_host_all_from_host(self,params):
        datacenter = self.create_datacenter( params.get_cluster().get_data_center())
        cluster = self.create_cluster(params.get_cluster())
        host = self.create_host_and_wait_for_host_up(params)
        return ReturnAll(datacenter,cluster,host) 

    def create_host_and_wait_for_host_up(self, params):
        host = self.create_host(params)
        Waiter.waitUntil(lambda : Waiter.host_is_up(self.api,host), 400)
        return host

    def deactivate_host_and_wait_for_maintanence(self,host):
        HostRepository(self.api).deactivate(host)
        Waiter.waitUntil(lambda : Waiter.host_is_maintanence(self.api,host), 200)

    def create_volume(self,cluster,params):
        return VolumeRepository(self.api).create(cluster,params)
