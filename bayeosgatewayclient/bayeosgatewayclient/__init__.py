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
    
# def sampleclient():
#     import sampleclient