'''creates an example writer'''

from array import array
from time import sleep

from bayeosGatewayClient import BayEOSWriter


def main():
    path = '/tmp/bayeos-device1/'
    writer = BayEOSWriter(path, 100)
    count = 0
    while True:
        print('adding frame\n')
        BayEOSWriter.saveDataFrame(writer, [[0,2], [1,3], [2,20]], 0x21, 0)
        count += 1
        sleep(1)
        
main()