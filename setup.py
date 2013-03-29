"""
Setup file for packaging flicktid
"""

import sys
import os

from setuptools import setup, find_packages

VERSION = '0.1.0'

META = {
    'name': 'flicktid',
    'version': VERSION,
    'description': 'Create tiddlyweb proxy tiddlers of a flick photo set',
    'long_description': file(os.path.join(
        os.path.dirname(__file__), 'README')).read(),
    'author': 'Chris Dent',
    'author_email': 'cdent@peermore.com',
    'url': 'http://pypi.python.org/pypi/flicktid',
    'packages': find_packages(),
    'scripts': ['bin/flicktid'],
    'platforms': 'Posix; MacOS X',
    'install_requires': ['docopt', 'requests'],
    'zip_safe': False,
}


if __name__ == '__main__':
    setup(**META)
