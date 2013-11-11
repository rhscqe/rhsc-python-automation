
from ovirtsdk.xml import params
class VolumeFactory:
    def distributedVolume(name):
       bricks = ParamFactory().create_bricks()
       for _ in range(4):
           bricks.add_brick(ParamFactory().create_brick(TestVolume.host.id))
       for _ in range(4):
           bricks.add_brick(ParamFactory().create_brick(TestVolume.host2.id))
       return ParamFactory().create_volume(bricks,name )

