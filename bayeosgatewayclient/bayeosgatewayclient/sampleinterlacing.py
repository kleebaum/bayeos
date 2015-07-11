"""Creates an example writer and sender using one loop."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter, BayEOSSender

PATH = '/tmp/bayeos-device/'
NAME = 'Python-Interlacing-Example'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
writer = BayEOSWriter(PATH, max_chunk=100)
writer.save_msg('Writer was started.')
sender = BayEOSSender(PATH, NAME, URL, 'import', 'import')

time_counter = 0

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2)
    time_counter += 1
    if time_counter % 5 == 0: # if True writer gaps are created
        res = sender.send()
        if res > 0:
            print 'Successfully sent ' + str(res) + ' frames.\n'
        time_counter = 0
    sleep(1)