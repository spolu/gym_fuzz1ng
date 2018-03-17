import os
import subprocess
import sys

from setuptools import setup
from distutils.command.build import build as DistutilsBuild

class Build(DistutilsBuild):
    def run(self):
        try:
            subprocess.check_call('cp -R ../mods .', cwd='build', shell=True)
            subprocess.check_call(['make'], cwd='build/mods')
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Could not build afl: %s.\n" % e)
            raise
        DistutilsBuild.run(self)

if not os.path.exists('build'):
    os.makedirs('build')

setup(
    name='gym_fuzz1ng',
    version='0.0.1',
    install_requires=['gym>=0.10.3'],
    author='Stanislas Polu',
    packages=['gym_fuzz1ng'],
    cmdclass={'build': Build },
    include_package_data=True
)
