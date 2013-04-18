from ovirtsdk.api import API

class ApiFactory:
    def api(self,api_actions):
        api = self.get_api()
        api_actions(api)
        api.close

    def get_api(self,url='https://localhost:443', username='admin@internal', password='redhat',insecure=True ):
        return API(url=url, username=username, password=password,insecure=insecure)
