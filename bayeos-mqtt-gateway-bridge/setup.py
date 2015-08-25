try:
    from setuptools import setup
except ImportError:
	from distutils.core import setup 

setup(name='bayeos-mqtt-gateway-bridge',
      version='1.0',
      description='BayEOS MQTT Bridge',
      url='',
      author='Oliver Archner',
      author_email='oliver.archner@uni-bayreuth.de',
      license='GPL2',
      packages=['bayeos'],
      package_dir = {'': 'src'})

