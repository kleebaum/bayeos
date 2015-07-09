"""Creates an example writer."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter

PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 50)

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2, origin='Herkunft')
    #writer.save_msg("message", error=True, origin='Herkunft')
    sleep(1)
