import logging
import os
import subprocess
import os
import signal
import subprocess
from time import sleep
import requests
import urllib
import types

from nose2.events import Plugin

log = logging.getLogger('prevent-teardown')


class SkipTeardown(Plugin):
    #configSection = 'helloworld'
    commandLineSwitch = (None, 'skipTeardown', 'Skipping Teardowns')

    def startTest(self, event):
        def tearDown(cls):
            print "skip teardown"
        event.test.tearDown=types.MethodType(tearDown,event.test)



