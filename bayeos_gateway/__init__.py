from struct import *

from bayeos_gateway.bayeosWriter import BayEOSWriter


def main():
    writer = BayEOSWriter('/home')
    BayEOSWriter.saveDataFrame(writer, [[0,2], [1,3], [2,20]], 0x01, -1)
main()    
    