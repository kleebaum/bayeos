"""bayeosraspberrypi setup"""

try:
    from setuptools import setup
except ImportError as ierr:
    print 'Import error :' + str(ierr)
    from distutils.core import setup

setup(
    name='bayeosraspberrypi',
    version='0.2',
    packages=['bayeosraspberrypi'],
    install_requires=['bayeosgatewayclient'],
    data_files=[('config',['bayeosraspberrypi/raspberryPi.ini'])],
    description='Module for writing data frames and sending them to a BayEOS gateway',
    author='Anja Kleebaum',
    author_email='Anja.Kleebaum@stmail.uni-bayreuth.de',
    license='GPL2',
    keywords='bayeos gateway client raspberry pi',
    classifiers=['Programming Language :: Python'])
