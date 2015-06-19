"""bayeosgatewayclient"""

from bayeosgatewayclient import *

def samplesender():    
    """Creates an example sender."""
    PATH = '/tmp/bayeos-device1/'
    NAME = 'Python-Test-Device'
    URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
    sender = BayEOSSender(PATH, NAME, URL, 'bayeos', 'root')

    while True:
        res = sender.send()
        if res > 0:
            print 'Successfully sent ' + str(res) + ' post requests.\n'
        sleep(5)
    
def samplewriter():
    """Creates an example writer."""
    PATH = '/tmp/bayeos-device1/'
    writer = BayEOSWriter(PATH, 100)
    
    while True:
        print 'adding frame\n'
        writer.save(values=[2.1, 3, 20.5], valueType=0x02, offset=2)
        writer.saveMessage("Dies ist noch eine weitere Nachricht...")
        writer.saveErrorMessage("Fehlermeldung")
        sleep(1)
    
def sampleclient():
    from random import randint

    OPTIONS = {'bayeosgateway_url' : 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat',
               'bayeosgateway_pw' : 'bayeos',
               'bayeosgateway_user' : 'root',
               'sender' : 'anja'}
    
    NAMES = ['PythonTestDevice1', 'PythonTestDevice2', 'PythonTestDevice3']
    
    class PythonTestDevice(BayEOSGatewayClient):
        """Creates both a writer and sender instance for every NAME. Implements BayEOSGatewayClient."""
        def readData(self):
            if self.names[self.i] == 'PythonTestDevice1':
                return (randint(-1, 1), 3, 4)
            else:
                return (2, 1.0, randint(-1, 1))
    print OPTIONS
    
    client = PythonTestDevice(NAMES, OPTIONS)    
    client.run()