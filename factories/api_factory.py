from ovirtsdk.api import API

class ApiFactory:
    def api(self,api_actions):
        api = self.get_api()
        api_actions(api)
        api.close

    def get_api(self):
        return API(url='https://localhost:443', username='admin@internal', password='redhat',insecure=True )
