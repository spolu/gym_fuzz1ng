import os

from setuptools import setup
from distutils.command.build import build as DistutilsBuild

class Build(DistutilsBuild):
    def run(self):
        pass

if not os.path.exists('gym_fuzz1ng'):
    os.makedirs('gym_fuzz1ng')

setup(
    name='gym_fuzz1ng',
    version='0.0.1',
    install_requires=['gym>=0.10.3'],
    author='Stanislas Polu',
    packages=['gym_fuzz1ng'],
    cmdclass={'build': Build },
    include_package_data=True
)
