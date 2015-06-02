try:
    from setuptools import setup
except ImportError as ierr:
    print('Import error :' + str(ierr))
    from distutils.core import setup

setup(  name = 'bayeosgatewayclient',
        version = '0.1',
        packages = ['bayeosgatewayclient', 'raspberryPi_py'],
        description = 'Module for writing data frames and sending them to a BayEOS gateway',
        author = 'Anja Kleebaum',
        author_email = 'Anja.Kleebaum@stmail.uni-bayreuth.de',
        license = 'GPL2',
        keywords = 'bayeos gateway client',
        classifiers = ["Programming Language :: Python"])