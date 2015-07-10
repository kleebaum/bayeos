"""Creates an example writer."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter

PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 50)
writer.save_msg('Writer was started.', origin='Python-Writer-Example')

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], value_type=0x02, offset=2, origin='Python-Writer-Example')
    writer.save_msg("error message", error=True, origin='Python-Writer-Example')
    sleep(1)