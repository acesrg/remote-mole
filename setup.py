import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="remote_mole",
    version="1.0.4",
    author="Marco Miretti",
    author_email="marcomiretti@gmail.com",
    description=("Create moles on remote setups."),
    license="GPLv3",
    keywords="bots ssh jupyter ngrok discord",
    url="http://packages.python.org/remote_mole",
    packages=[
        'remote_mole.{}'.format(sub_pkg) for sub_pkg in find_packages(
            where='src/remote_mole'
        )
    ],
    package_dir={'': 'src'},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'pyngrok==5.0.5',
        'discord.py==1.7.3',
        'questionary==1.9.0',
    ],

    entry_points={
        'console_scripts': [
            'remote_mole = remote_mole.setup.entrypoint:main',
        ]
    },
)
