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

log = logging.getLogger('skip-teardown')


class SkipTeardown(Plugin):
    configSection = 'skip-teardown'
    commandLineSwitch = (None, 'skip-teardown', 'Skipping Teardowns')

    def startTest(self, event):
        def tearDown(self):
            log.info("skip teardown")
        def tearDownClass(cls):
            log.info("skip tearDownClass")
        event.test.tearDown=types.MethodType(tearDown,event.test)
        event.test.__class__.tearDownClass=types.MethodType(tearDownClass,event.test.__class__)



