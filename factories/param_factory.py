
from ovirtsdk.xml import params
from ovirtsdk.xml import params
from ovirtsdk.infrastructure.errors import RequestError
from ovirtsdk.api import API
from time import gmtime, strftime
import datetime
from random import randint

class ParamFactory:
    def generate_brick_dir(self):
        return "{0}-{1}".format(datetime.datetime.now().strftime("/tmp/brick%y%m%d%H%M%S%f"),randint(0,10000))

    def create_datacenter(self, name="mydatacenter", description="hi", storage_type="posixfs", version=None):
        version = version or self.create_version()
        return params.DataCenter(name=name, description=description, storage_type=storage_type, version=version)

    def create_datacenter_from(self,datacenter_broker):
        return params.DataCenter(id=datacenter_broker.id)

    def create_version(self,major='3',minor='1'):
        return params.Version(major=major, minor=minor)

    def create_cpu(self,id='Intel SandyBridge Family'):
        return params.CPU(id=id)

    def create_cluster(self, name="mycluster", cpu=None, datacenter=None, datacenter_broker=None, version=None, virt_service=False, gluster_service=True):
        version = version or self.create_version()
        cpu = cpu or self.create_cpu()
        if(datacenter):
            datacenter_param = datacenter
        elif (datacenter_broker):
            datacenter_param = self.create_datacenter_from(datacenter_broker)
        else:
            datacenter_param= None
        return params.Cluster(name="mycluster", cpu=cpu, data_center=datacenter_param, version=version, virt_service=virt_service, gluster_service=gluster_service)

    def create_host(self, cluster,name, host, root_password="redhat"):
        return params.Host(name=name, address=host, cluster=cluster, root_password="redhat", reboot_after_installation=False )

    def create_brick(self,host_id,dir=None):
        dir = dir or self.generate_brick_dir()
        return params.GlusterBrick(server_id=host_id, brick_dir=dir)

    def create_bricks(self,*bricks):
        result = params.GlusterBricks()
        for brick in bricks:
            result.add_brick(brick)
        return result

    def create_volume(self,bricks, name, volume_type="DISTRIBUTE"):
        return params.GlusterVolume(name=name, volume_type=volume_type, bricks=bricks)
