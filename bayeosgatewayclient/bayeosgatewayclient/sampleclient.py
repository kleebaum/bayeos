"""Creates an example client."""

from bayeosgatewayclient import BayEOSGatewayClient
from random import randint

OPTIONS = {'bayeosgateway_url' : 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat',
           'bayeosgateway_pw' : 'xbee',
           'bayeosgateway_user' : 'admin',
           'sender' : 'anja'}

NAMES = ['PythonTestDevice1', 'PythonTestDevice2', 'PythonTestDevice3']
#names = ['PythonTestDevicex']

class PythonTestDevice(BayEOSGatewayClient):
    """Creates both a writer and sender instance for every NAME. Implements BayEOSGatewayClient"""
    def readData(self):
        if self.names[self.i] == 'PythonTestDevice1':
            return (randint(-1, 1), 3, 4)
        else:
            #return [[0,2], [1,1.0], [2,randint(-1,1)]]
            return (2, 1.0, randint(-1, 1))
print OPTIONS

client = PythonTestDevice(NAMES, OPTIONS)

client.run()
