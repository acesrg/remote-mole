import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="remote_ninja",
    version="0.1.0",
    author="Marco Miretti",
    author_email="marcomiretti@gmail.com",
    description=("Create ninjas on remote setups."),
    license="GPLv3",
    keywords="bots ssh jupyter ngrok discord",
    url="http://packages.python.org/remote_ninja",
    packages=[
        'remote_ninja.{}'.format(sub_pkg) for sub_pkg in find_packages(
            where='src/remote_ninja'
        )
    ],
    package_dir={'': 'src'},
    long_description=read('readme.md'),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'remote_ninja = remote_ninja.setup.entrypoint:register',
        ]
    },
)
