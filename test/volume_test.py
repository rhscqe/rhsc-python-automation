from test.test_base          import TestBase
from fixture.fixtures        import FixtureFactory
from factories.param_factory import ParamFactory
from repository.repositories import HostRepository
from ovirtsdk.infrastructure.errors import RequestError
from config.config import Config 

class TestVolume(TestBase):
    def setUp(self):
        super(TestVolume, self).setUp()
        self.host = FixtureFactory().create_host_all_from_host(self.api, Config.get_instance().get_host_by_name('myhost')).host
        result = FixtureFactory().create_host_all_from_host(self.api, Config.get_instance().get_host_by_name('myhost2'))
        self.host2 = result.host
        self.cluster = result.cluster


    def tearDown(self):
        super(TestVolume, self).tearDown()

        #Host.stop_and_wait_for_status_maintanence(api,host)
        #self.host.delete()
        #Host.stop_and_wait_for_status_maintanence(api,host2)
        #self.host2.delete()
        #self.cluster.delete()
        #self.datacenter.delete()

    def test_negative_create_distributed_volume_with_bricks_from_another(self):
        vol = None
        existing_volum = None
        try:
            existing_volum = self.__create_distributed_volume('existing-volume')
            existing_brick = existing_volum.bricks.list()[0]

            bricks = self.__create_param_bricks(self.host.id, 7)
            bricks.append(ParamFactory().create_brick(existing_brick.get_server_id(),existing_brick.get_brick_dir()))
            self.assertRaisesRegexp(RequestError,'.*already in use.*',
                    lambda: FixtureFactory().create_volume(self.cluster, ParamFactory().create_volume(ParamFactory().create_bricks(*bricks),'existing-brick-negative-volume')))
        finally:
            existing_volum and existing_volum.delete()
            vol and vol.delete()


    def test_create_distributed_volume(self):
       bricks = ParamFactory().create_bricks()
       for _ in range(4):
           bricks.add_brick(ParamFactory().create_brick(self.host.id))
       for _ in range(4):
           bricks.add_brick(ParamFactory().create_brick(self.host2.id))
       volparams = ParamFactory().create_volume(bricks,'myvol2')
       vol = FixtureFactory().create_volume(self.cluster, volparams)
       vol.delete()

    def test_create_replicated_volume(self):
        bricks = ParamFactory().create_bricks()
        for _ in range(4):
            bricks.add_brick(ParamFactory().create_brick(self.host.id))
        for _ in range(4):
            bricks.add_brick(ParamFactory().create_brick(self.host2.id))
        volparams = ParamFactory().create_volume(bricks,'rep-vol',"REPLICATE")
        volparams.set_replica_count(8)
        vol = FixtureFactory().create_volume(self.cluster, volparams)
        vol.delete()

    def test_add_brick(self):
        vol = self.__create_distributed_volume('test-add-brick')

        new_bricks= ParamFactory().create_bricks(ParamFactory().create_brick(self.host2.id))
        vol.bricks.add(new_bricks)
        vol.delete()

    def __create_param_bricks(self,host_id,num_bricks):
        result = []
        for _ in range(num_bricks):
            result.append(ParamFactory().create_brick(host_id))
        return result

    def __create_distributed_volume_params(self, name):
        bricks = ParamFactory().create_bricks()
        for _ in range(4):
            bricks.add_brick(ParamFactory().create_brick(self.host.id))
        for _ in range(4):
            bricks.add_brick(ParamFactory().create_brick(self.host2.id))
        volparams = ParamFactory().create_volume(bricks, name)
        return volparams

    def __create_distributed_volume(self, name):
        return FixtureFactory().create_volume(self.cluster, self.__create_distributed_volume_params(name))
