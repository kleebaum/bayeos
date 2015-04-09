'''creates an example sender'''

from time import sleep

from bayeosGatewayClient import BayEOSSender


def main():
    path = '/tmp/bayeos-device1/'
    name = 'PythonTest3'
    url = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
    sender = BayEOSSender(path, name, url, 'xbee', 'admin')
    
    while True:
        sender.send()
#         if status > 0:
#             print ("juhu!\n")
        sleep(5)  
        
main()