"""Creates an example writer and sender using Unix fork."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from os import fork

PATH = '/tmp/bayeos-device/'
NAME = 'Python-Fork-Example'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'

pid = fork()
if pid > 0:
    print 'Hello from parent writer!'
    writer = BayEOSWriter(PATH, max_chunk=100)
    writer.save_msg('Writer was started.')
    while True:
        print 'adding frame'
        writer.save(values=[2.1, 3, 20.5])
        sleep(1)
elif pid == 0:
    print 'Hello from child sender!'
    sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')
    sender.run(5)
else:
    exit('Fork error.')