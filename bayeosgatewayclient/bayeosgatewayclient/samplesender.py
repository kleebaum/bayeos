"""Creates an example sender."""

from time import sleep
from bayeosgatewayclient import BayEOSSender

PATH = '/tmp/bayeos-device1/'
NAME = 'Python-Test-Device'
URL = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
sender = BayEOSSender(PATH, NAME, URL, 'bayeos', 'root')

while True:
    res = sender.send()
    if res > 0:
        print 'Successfully sent ' + str(res) + ' post requests.\n'
    sleep(5)
