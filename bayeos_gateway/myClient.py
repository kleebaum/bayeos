from bayeosGatewayClient import BayEOSGatewayClient
from random import randint

options = {'bayeosgateway_url' : 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat',
           'bayeosgateway_pw' : 'xbee',
           'bayeosgateway_user' : 'admin',
           'sender' : 'anja'}

names = ['Python-Test/Device\\"\'1', 'Python-TestDevice2']

class PythonTestDevice(BayEOSGatewayClient):
    
    def readData(self):
        if self.names[self.i] == 'Python-TestDevice1':
            return False
        else:
            #return [[0,2], [1,1.0], [2,randint(-1,1)]]
            return (2, 1.0, randint(-1,1))

client = PythonTestDevice(names, options)

client.run()