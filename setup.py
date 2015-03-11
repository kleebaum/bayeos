try:
    from setuptools import setup
except ImportError ierr:
    print('Import error :' + str(ierr))
    from distutils.core import setup

setup(  name = 'bayeos-gateway-py',
        version = '0.1',
        description = 'Module for accesing the BayEOS gateway',
        author = 'Anja Kleebaum',
        author_email = 'Anja.Kleebaum@stmail.uni-bayreuth.de')
