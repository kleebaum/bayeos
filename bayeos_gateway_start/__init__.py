from bayeos_gateway_start.bayeos import saveDataFrame, toString
from struct import *

def main():
    saveDataFrame([2, 40, 3, 50])
    f = open ('/home/anja/tmp/bayeos-device1/1426779597-0.50015300.act', 'rb')
    zeile = f.readline()
    print(len(zeile))
    print(zeile)
    print('Frame with header: ', toString(zeile, True))
    f.close()
main()    
    