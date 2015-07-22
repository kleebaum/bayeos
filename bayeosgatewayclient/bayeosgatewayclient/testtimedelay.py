"""Script to test the time delay during writing."""

from time import time, sleep, strptime, strftime, mktime
from bayeosgatewayclient import BayEOSWriter, BayEOSSender
from thread import start_new_thread

PATH = '/tmp/bayeos-device2/'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
writer = BayEOSWriter(PATH, 50)
writer.save_msg('Writer was started.')

sender = BayEOSSender(PATH, 'Python-Writer-Test-Anja', URL, 'import', 'import')
start_new_thread(sender.run, (5,))

today=mktime(strptime(strftime('%Y-%m-%d'),'%Y-%m-%d'))
start=time()
while True:
    t=time()
    writer.save([t-start, t-today], value_type=0x21)
    sleep(1)