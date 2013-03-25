
from ovirtsdk.xml import params

from ovirtsdk.api import API
from ovirtsdk.infrastructure.brokers import ClusterGlusterVolumes
from time import gmtime, strftime
from random import randint


#VERSION = params.Version(major='3', minor='1')

#api = API(url='https://localhost:443', username='admin@internal', password='redhat',insecure=True )
#cpu = params.CPU(id='Intel SandyBridge Family')
#dc = api.datacenters.get('Default')
#dc = api.datacenters.add(params.DataCenter(name="mydatacenter", description="hi", storage_type="posixfs", version=VERSION))
#api.clusters.add(params.Cluster(name="mycluster", cpu=cpu, data_center=dc, version=VERSION, virt_service=False, gluster_service=True))


#cluster = api.clusters.get("mycluster")
#api.hosts.add(params.Host(name="rhevm-sf101-node-a", address="rhevm-sf101-node-a", cluster=cluster, root_password="redhat" ))

#host =api.hosts.get('rhevm-sf101-node-a')
#host.get_status().get_state()
#import pdb; pdb.set_trace()
#brick = params.GlusterBrick(server_id=host.id, brick_dir='/tmp/brick')
#bricks = params.GlusterBricks()
#bricks.add_brick(brick)
#api.clusters.get("mycluster").glustervolumes.add(params.GlusterVolume(name="myvolume", volume_type="DISTRIBUTE", bricks=bricks))

#import unittest so old guise
import unittest2 as unittest
import logging
logging.basicConfig(level=logging.DEBUG)

from time import sleep
import datetime

class ApiFactory:
    def api(self,api_actions):
        api = self.get_api()
        api_actions(api)
        api.close

    def get_api(self):
        return API(url='https://localhost:443', username='admin@internal', password='redhat',insecure=True )

class Waiter:
    @classmethod
    def waitUntil(cls,condition, attempts=10):
        logging.debug("waiting...for " + condition.__name__)
        for attempt in range(attempts):
            logging.debug("attempt {0} of {1}".format(attempt, attempts))
            sleep(1)
            if condition():
                return True
        return False

    @classmethod 
    def refresh_host(cls,api,host):
        return api.hosts.get(id=host.id)

    @classmethod
    def host_is_up(cls,api,host):
        host = cls.refresh_host(api,host)
        return host.get_status().get_state() == 'up'

    @classmethod
    def host_is_maintanence(cls,api,host):
        host = cls.refresh_host(api,host)
        print "in state %(current_state)s waiting for %(state)s" % {"current_state": host.get_status().get_state(), "state": "maintenance"}
        return host.get_status().get_state() == 'maintenance'

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

    def create_cluster(self, name="mycluster", cpu=None, datacenter_broker=None, version=None, virt_service=False, gluster_service=True):
        version = version or self.create_version()
        cpu = cpu or self.create_cpu()
        datacenter_param = self.create_datacenter_from(datacenter_broker) if datacenter_broker else None
        return params.Cluster(name="mycluster", cpu=cpu, data_center=datacenter_param, version=version, virt_service=virt_service, gluster_service=gluster_service)

    def create_host(self, cluster_broker,name, host, root_password="redhat"):
        return params.Host(name=name, address=host, cluster=cluster_broker, root_password="redhat" )

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

class Datacenter:
    @classmethod
    def create(cls,api,params=ParamFactory().create_datacenter()):
        return api.datacenters.add(params) 

class Cluster:
    @classmethod
    def create(cls,api,params=ParamFactory().create_cluster()):
        return api.clusters.add(params)

class Host:
    @classmethod
    def create(cls,api,params):
        return api.hosts.add(params) 

    @classmethod 
    def refresh(cls,api,host):
        return api.hosts.get(id=host.id)

    @classmethod 
    def stop_and_wait_for_status_maintanence(cls,api,host):
        host.deactivate()
        Waiter.waitUntil(lambda : Waiter.host_is_maintanence(api,host), 200)

class Volume:
    @classmethod
    def create(cls,cluster,params):
        return cluster.glustervolumes.add(params)


class FixtureFactory:
    def create_datacenter(self,api,params=ParamFactory().create_datacenter()):
        return api.datacenters.get(params.get_name()) or Datacenter.create(api,params)

    def create_cluster(self,api,params=ParamFactory().create_cluster()):
        return api.clusters.get(params.get_name()) or Cluster.create(api,params)

    def create_host(self,api, params):
        return api.hosts.get(params.get_name()) or Host.create(api,params)

    def create_host_and_wait_for_host_up(self,api, params):
        host = self.create_host(api,params)
        Waiter.waitUntil(lambda : Waiter.host_is_up(api,host), 400)
        return host

    def create_volume(self,cluster,params):
        return Volume.create(cluster,params)

class TestBase(unittest.TestCase):
    def setUp(self):
        self.api        = ApiFactory().get_api()

    def tearDown(self):
        self.api.disconnect()

import re
class ProductInfoTest(TestBase):
    def test_product_info(self):
        self.api.get_product_info()

    def test_version(self):
        version = self.api.get_product_info().get_version()
        self.assertTrue(re.match(r'\d',str(version.get_major())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_minor())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_build())), "major version could not be obtained")
        self.assertTrue(re.match(r'\d',str(version.get_revision())), "major version could not be obtained")

    

class TestVolume(unittest.TestCase):
    def setUp(self):
        self.api        = ApiFactory().get_api()
        self.datacenter = FixtureFactory().create_datacenter(self.api)
        self.cluster    = FixtureFactory().create_cluster(self.api,params=ParamFactory().create_cluster(datacenter_broker=self.datacenter))
        self.host       = FixtureFactory().create_host_and_wait_for_host_up(self.api, ParamFactory().create_host(self.cluster,"myhost","rhevm-sf101-node-a"))
        self.host2       = FixtureFactory().create_host_and_wait_for_host_up(self.api, ParamFactory().create_host(self.cluster,"myhost2","rhevm-sf101-node-b"))
        self.assertEqual(Host.refresh(self.api,self.host).get_status().get_state(), "up")
        self.assertEqual(Host.refresh(self.api,self.host2).get_status().get_state(), "up")

    def tearDown(self):
        #Host.stop_and_wait_for_status_maintanence(api,host)
        #self.host.delete()
        #Host.stop_and_wait_for_status_maintanence(api,host2)
        #self.host2.delete()
        #self.cluster.delete()
        #self.datacenter.delete()
        self.api.disconnect()

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


if __name__ == '__main__':
            unittest.main()
