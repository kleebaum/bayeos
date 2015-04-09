from struct import *

from bayeos_gateway.bayeosGatewayClient import BayEOSWriter


def main():
    writer = BayEOSWriter('/home/anja/tmp/test6/')
    BayEOSWriter.saveDataFrame(writer, [[0,2], [1,3], [2,20]], 0x01, 0)
main()    
    