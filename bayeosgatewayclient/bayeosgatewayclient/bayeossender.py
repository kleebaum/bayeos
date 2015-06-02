from time import sleep
from .bayeosgatewayclient import BayEOSSender

"""Creates an example sender."""
path = '/tmp/bayeos-device1/'
name = 'Python-Test-Device'
url = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
sender = BayEOSSender(path, name, url, 'xbee', 'admin')
    
while True:
    res = sender.send()
    if res > 0:
        print ('Successfully sent ' + str(res) + ' post requests.\n')
    sleep(5)  
        
