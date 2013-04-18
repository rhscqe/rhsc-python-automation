from factories.param_factory import ParamFactory
from ovirtsdk.xml import params
from ovirtsdk.infrastructure.errors import RequestError
from ovirtsdk.api import API
import jsonpickle



class Item(object):
    def __init__(self, args, extras={},creation=None):
        self.args = args
        self.extras = extras
        self.creation=creation


    def transform_extras(self):
        result = {}
        for key in self.extras:
            result[key] = self.extras[key].create()
        return result

    def compiled_args(self):
        result = {}
        result.update(self.args)
        result.update(self.transform_extras())
        return result

    def create(self):
        return self.creation(**compiled_args())



class Version(Item):
    def __init__(self,args,extras={}):
        Item.__init__(self,args,extras )

    def create(self):
        return ParamFactory().create_version(**self.compiled_args())


class Datacenter(Item):
    def __init__(self,args,extras={}):
        Item.__init__(self,args,extras )

    def create(self):
        return ParamFactory().create_datacenter(**self.compiled_args())


class Cluster(Item):
    def __init__(self,args,extras={}):
        Item.__init__(self,args,extras )

    def create(self):
        return ParamFactory().create_cluster(**self.compiled_args())

class CPU(Item):
    def __init__(self,args,extras={}):
        Item.__init__(self,args,extras )

    def create(self):
        return ParamFactory().create_cpu(**self.compiled_args())

class Host(Item):
    def __init__(self,args,extras={}):
        Item.__init__(self,args,extras )

    def create(self):
        return ParamFactory().create_host(**self.compiled_args())



class Config:
    def __init__(self):
        self.rest_api= {'url':'https://localhost:443/api', 'credentials': {'username':'admin@internal', 'password':'CHANGEME'}}
        self.version = Version({'major':'3', 'minor':'1'})
        self.datacenter = Datacenter({'name':'mydatacenter', 'description':'a description', 'storage_type':'posixfs'} ,{'version':self.version})
        cpu = CPU({'id':'Intel SandyBridge Family'})
        self.cluster = Cluster({'name':"mycluster", 'virt_service':False, 'gluster_service':True} , { 'datacenter':self.datacenter , 'version':self.version, 'cpu': cpu })
        self.hosts = []
        self.hosts.append( Host({'name':'myhost', 'host':'rhevm-sf101-node-a', 'root_password':"CHANGEME"}, {'cluster':self.cluster}))
        self.hosts.append( Host({'name':'myhost2', 'host':'rhevm-sf101-node-a', 'root_password':"CHANGEME"}, {'cluster':self.cluster}))


    def to_json(self):
      return jsonpickle.encode(self)

    def get_host_by_name(self,name):
        return filter(lambda x: x.compiled_args()['name']== name , self.hosts)[0].create()

    @classmethod
    def from_json(cls,json):
        return jsonpickle.decode(json)

    @classmethod
    def get_instance(cls):
        json = open('config/config.json', 'r').read()
        return Config.from_json(json)


if __name__ == "__main__":

    json =  Config().to_json()
    print json
#    #print Config().from_json(json).datacenter.create()
#    import pdb; pdb.set_trace()
#    print Config().from_json(json).hosts[0].create().get_cluster().get_data_center().get_name()
#    print Config().from_json(json).hosts[0].create().get_cluster().get_data_center().get_name()




    #json = open('config/config.json', 'r').read()
    #config = Config.from_json(json)
    #myhost = config.get_host_by_name('node1')
    #print myhost.get_name()
