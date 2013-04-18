import logging
import os
import subprocess
import os
import signal
import subprocess
from time import sleep
import requests
import urllib

from nose2.events import Plugin

log = logging.getLogger('nose2.plugins.helloworld')
#log = logging.getLogger('blah')

class ReportEngineForwarderApi:
    def __init__(self, base="http://localhost:27514"):
        self.base = base #scheme and authority

    def get(self,path_and_query):
        return requests.get(self.base + path_and_query)

    def createReport(self,name):
        return self.get("/report/create?" 
                +  urllib.urlencode({'name': name}))

    def finishReport(self):
        return self.get("/report/finish")

    def createTestGroup(self, name="tests"):
        return self.get("/testgroup/create")#?" +  urllib.urlencode({'name': name}))

    def startTest(self, name):
        return self.get("/testcase/start?"
                +  urllib.urlencode({'name': name}))

    def passTest(self):
        return self.get("/testcase/pass")

    def failTest(self):
        return self.get("/testcase/fail")


class ReportEngine(Plugin):
    #configSection = 'helloworld'
    commandLineSwitch = (None, 'reportengine', 'Say hello!')

    def startTestRun(self, event):
        log.info('Hello pluginized world!')
        self.process = subprocess.Popen("java -jar reportengineforwarder.jar", stdout=subprocess.PIPE, 
                                       shell=True, preexec_fn=os.setsid) 
        if(self.is_process_running(self.process.pid)):
            log.info('report engine forwarder started')
        else:
            log.info('report engine forwarder could not be started')
        self.api = ReportEngineForwarderApi()

        sleep(2)
        self.api.createReport("RHEVM-PYTHON_SDK-INTEGRATION")
        self.api.createTestGroup()



    def stopTestRun(self, event):
        self.api.finishReport()
        os.killpg(self.process.pid, signal.SIGTERM)

    def startTest(self, event):
        test = event.test
        name = test.__module__ + "." + test.__class__.__name__ + ":" +  test._testMethodName
        self.api.startTest(name)

    def stopTest(self, event):
        if(event.result.wasSuccessful()):
            self.api.passTest()
        else:
            self.api.failTest()


    def is_process_running(self,process_id):
        try:
            os.kill(process_id, 0)
            return True
        except OSError:
            return False
