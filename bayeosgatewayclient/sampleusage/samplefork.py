"""Creates an example writer and sender using Unix fork."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from os import fork

PATH = '/tmp/bayeos-device2/'
NAME = 'Python-Fork-Example'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

pid = fork()
if pid > 0:
    print "Hello from Parent Writer"
    writer = BayEOSWriter(PATH, max_chunk=100)
    writer.save_msg('Writer was started.')
    while True:
        print 'adding frame\n'
        writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2)
        sleep(1)
elif pid == 0:
    print "Hello from Child Sender"
    sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')
    sender.run(5)
else:
    exit("Fork error.")