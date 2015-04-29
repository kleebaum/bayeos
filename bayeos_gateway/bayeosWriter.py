from time import sleep
from bayeosGatewayClient import BayEOSWriter

"""Creates an example writer."""
path = '/tmp/bayeos-device1/'
writer = BayEOSWriter(path, 100)
    
while True:
    print('adding frame\n')
    writer.save(offset=2, values=(2,3,20))
    sleep(1)
