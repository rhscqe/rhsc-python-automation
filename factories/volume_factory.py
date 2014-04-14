from ovirtsdk.xml import params
from factories.param_factory import ParamFactory
from factories.param_factory import BrickFactory
#
class VolumeFactory:
    def __init__(self,brick_factory=BrickFactory()):
        self.brick_factory= brick_factory;

    def create_bricks(self, hosts, num_bricks):
        bricks = ParamFactory().create_bricks()
        for i in range(num_bricks):
            host_index = i % len(hosts)
            bricks.add_brick(BrickFactory().create(hosts[host_index].id))
        return bricks;

    def create_volume(self, name, hosts, volume_type, num_bricks, replica_count, stripe_count=None, **kwargs):
        bricks = self.create_bricks(hosts, num_bricks)
        return params.GlusterVolume(name=name,volume_type=volume_type, replica_count=replica_count, stripe_count=stripe_count, bricks=bricks,**kwargs)

    def create_distributed_replicate_volume(self, name, hosts, num_bricks, replica_count, **kwargs):
       return self.create_volume(name, hosts, "DISTRIBUTED_REPLICATE", num_bricks, replica_count, None, **kwargs)

    def create_distributed_volume(self, name, hosts, num_bricks, **kwargs):
        return self.create_volume(name, hosts, "DISTRIBUTE", num_bricks, None, None, **kwargs)
