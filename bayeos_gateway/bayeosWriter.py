from time import sleep
from bayeosGatewayClient import BayEOSWriter

def main():
    """Creates an example writer."""
    path = '/tmp/bayeos-device1/'
    writer = BayEOSWriter(path, 100)
    
    while True:
        print('adding frame\n')
        BayEOSWriter.saveDataFrame(writer, [[0,2], [1,3], [2,20]], 0x21, 0)
        sleep(1)
        
main()