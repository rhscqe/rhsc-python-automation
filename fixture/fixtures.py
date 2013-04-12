from repository.repositories import DatacenterRepository
from repository.repositories import ClusterRepository
from repository.repositories import HostRepository
from repository.repositories import VolumeRepository
from factories.param_factory import ParamFactory
from helpers.waiter import Waiter

class FixtureFactory:
    def create_datacenter(self,api,params=ParamFactory().create_datacenter()):
        return api.datacenters.get(params.get_name()) or DatacenterRepository.create(api,params)

    def create_cluster(self,api,params=ParamFactory().create_cluster()):
        return api.clusters.get(params.get_name()) or ClusterRepository.create(api,params)

    def create_host(self,api, params):
        return api.hosts.get(params.get_name()) or HostRepository.create(api,params)

    def create_host_and_wait_for_host_up(self,api, params):
        host = self.create_host(api,params)
        Waiter.waitUntil(lambda : Waiter.host_is_up(api,host), 400)
        return host

    def create_volume(self,cluster,params):
        return VolumeRepository.create(cluster,params)
