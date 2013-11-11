from test.test_base          import TestBase
from fixture.fixtures        import FixtureFactory
from factories.param_factory import ParamFactory
from repository.repositories import DatacenterRepository
from repository.repositories import ClusterRepository
from repository.repositories import HostRepository
from repository.repositories import VolumeRepository
from factories.param_factory import ParamFactory
from ovirtsdk.infrastructure.errors import RequestError
from config.config import Config
from ssh.remote_shell_factory import RemoteShellFactory
from ssh.dd import DD
from factories.volume_factory import VolumeFactory
from fixture.volume_populator import VolumePopulator

class RebalanceTest(TestBase):

    def setUp(self):
        self.api = TestBase.api
        self.host = FixtureFactory(self.api).create_host_with_depends(Config.get_instance().hosts[0].create()).host
        result = FixtureFactory(api).create_host_with_depends(Config.get_instance().hosts[1].create())
        self.host2 = result.host
        self.cluster = result.cluster
        self.datacenter = result.datacenter
        self.vol = create_distributed_volume()
        VolumePopulator().fileForEachBrick(volume)
        

    @classmethod
    def tearDown(self):
        FixtureFactory(self.api).deactivate_host_and_wait_for_maintanence(self.host)
        HostRepository(self.api).destroy(self.host)
        FixtureFactory(self.api).deactivate_host_and_wait_for_maintanence(self.host2)
        HostRepository(self.api).destroy(self.host2)
        ClusterRepository(self.api).destroy(self.cluster)
        DatacenterRepository(self.api).destroy(self.datacenter)
        self.vol.delete()

    def create_distributed_volume(self):
       params= VolumeFactory().distributedVolume('my_dist_vol')
       return FixtureFactory(self.api).create_volume(TestVolume.cluster, params)

