try:
    from setuptools import setup
except ImportError as ierr:
    print('Import error :' + str(ierr))
    from distutils.core import setup

setup(  name = 'bayeos-gateway-client-py',
        version = '0.1',
        packages = ['bayeos-gateway-client-py'],
        description = 'Module for accessing the BayEOS gateway',
        author = 'Anja Kleebaum',
        author_email = 'Anja.Kleebaum@stmail.uni-bayreuth.de')