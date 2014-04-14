from test.test_base          import TestBase
from fixture.fixtures        import FixtureFactory
from factories.param_factory import ParamFactory
from repository.repositories import DatacenterRepository
from repository.repositories import ClusterRepository
from repository.repositories import HostRepository
from repository.repositories import VolumeRepository
from factories.param_factory import ParamFactory
from factories.param_factory import BrickFactory
from factories.volume_factory import VolumeFactory
from ovirtsdk.infrastructure.errors import RequestError
from config.config import Config
from helpers.tcms import tcms

class TestVolume(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestVolume,cls).setUpClass()
        cls.host = FixtureFactory(cls.api).create_host_with_depends(Config.get_instance().hosts[0].create()).host
        result = FixtureFactory(cls.api).create_host_with_depends(Config.get_instance().hosts[1].create())
        cls.host2 = result.host
        cls.hosts = [cls.host, cls.host2]
        cls.cluster = result.cluster
        cls.datacenter = result.datacenter

    @classmethod
    def tearDownClass(cls):
        FixtureFactory(cls.api).deactivate_host_and_wait_for_maintanence(cls.host)
        HostRepository(cls.api).destroy(cls.host)
        FixtureFactory(cls.api).deactivate_host_and_wait_for_maintanence(cls.host2)
        HostRepository(cls.api).destroy(cls.host2)
        ClusterRepository(cls.api).destroy(cls.cluster)
        DatacenterRepository(cls.api).destroy(cls.datacenter)
        super(TestVolume,cls).tearDownClass()

    def test_create_distributed_volume(self):
        volparams = VolumeFactory().create_distributed_volume("myvol", TestVolume.hosts, 8 )
        vol = FixtureFactory(self.api).create_volume(TestVolume.cluster, volparams)
        vol.delete()

    def test_create_replicated_volume(self):
        volparams = VolumeFactory().create_distributed_replicate_volume("myvol", TestVolume.hosts, 8, 2 )
        vol = FixtureFactory(self.api).create_volume(TestVolume.cluster, volparams)
        vol.delete()

    @tcms(327430)
    def test_add_brick(self):
        volparams = VolumeFactory().create_distributed_volume("myvol", TestVolume.hosts, 8 )
        vol = FixtureFactory(self.api).create_volume(TestVolume.cluster, volparams)
        try:
            bricks = ParamFactory().create_bricks()
            new_brick= BrickFactory().create(TestVolume.host2.id)
            bricks.add_brick(new_brick)
            vol.bricks.add(bricks)
        except Exception as e:
            raise
        finally:
            vol.delete()


    def test_negative_create_distributed_volume_with_bricks_from_another(self):
        vol = None
        existing_volum = None
        try:
            existing_volume_params = VolumeFactory().create_distributed_volume("existing-volume", TestVolume.hosts, 8 )
            existing_volum = FixtureFactory(self.api).create_volume(TestVolume.cluster, existing_volume_params)
            existing_brick = existing_volum.bricks.list()[0]

            bricks = VolumeFactory().create_bricks(TestVolume.hosts, 7)
            bricks.add_brick( BrickFactory().create(existing_brick.get_server_id(),existing_brick.get_brick_dir()))
            new_volume_params =  VolumeFactory().create_distributed_volume("new-volume", TestVolume.hosts, 8 )
            new_volume_params.set_bricks(bricks)
            self.assertRaisesRegexp(RequestError,'.*already used.*',
                    lambda: FixtureFactory(self.api).create_volume(TestVolume.cluster, new_volume_params))
        finally:
            existing_volum and existing_volum.delete()
            vol and vol.delete()
