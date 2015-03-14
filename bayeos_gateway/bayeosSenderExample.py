'''creates an example sender'''

import bayeosSender
from array import array
from time import sleep

def main():
    sender = bayeosSender.BayEOSSender('/tmp/bayeos-device1',
                                       'PHP-Test-Device',
                                       'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat',
                                       'xbee',
                                       'admin')
    while True:
        pass
        