from bayeosGatewayClient import BayEOSGatewayClient
from random import randint

options = {}
options['bayeosgateway_url'] = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
options['bayeosgateway_pw'] = 'xbee'
options['bayeosgateway_user'] = 'admin'
options['tmp_dir'] = '/tmp/bayeos-device1'

names = ['Python-TestDevice1', 'Python-TestDevice2']

class PythonTestDevice(BayEOSGatewayClient):
    
    def readData(self):
        if self.names[self.i] == 'Python-TestDevice1':
            return False
        else:
            return [2, 1.0, randint(-1,1)]

client = PythonTestDevice(names, options)

client.run()