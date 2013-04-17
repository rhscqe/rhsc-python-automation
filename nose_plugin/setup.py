#!/usr/bin/env python

from distutils.core import setup

setup(name='ReporEngine',
      version='1.0',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='http://www.python.org/sigs/distutils-sig/',
      packages=['distutils', 'distutils.command'],
      entry_points = {
            'nose.plugins.0.10': [
                'someplugin = someplugin:SomePlugin'
                ]
            }
     )
