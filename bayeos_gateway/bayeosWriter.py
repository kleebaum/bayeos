from time import sleep
from bayeosGatewayClient import BayEOSWriter

"""Creates an example writer."""
path = '/tmp/bayeos-device1/'
writer = BayEOSWriter(path, 100)
    
while True:
    print('adding frame\n')
    writer.save(values=(2.1,3,20.5), valueType=0x02, offset=2)
    sleep(1)
