"""Creates an example writer and sender using threads."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from thread import start_new_thread

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
        
start_new_thread(samplesender, ())

"""Creates an example writer."""
PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 100)

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], valueType=0x02, offset=2)
    sleep(1)