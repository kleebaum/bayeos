from struct import *

from bayeos_gateway_start.bayeos import saveDataFrame, toString


def main():
    saveDataFrame([[0,2], [1,3], [2,20]], 0x01, -1)
main()    
    