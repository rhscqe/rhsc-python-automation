import logging
from time import sleep
logging.basicConfig(level=logging.DEBUG)

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
