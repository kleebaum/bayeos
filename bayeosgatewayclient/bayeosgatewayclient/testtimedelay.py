"""Script to test the time delay during writing."""

from time import time, sleep
import datetime
from bayeosgatewayclient import BayEOSWriter

PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 50)
writer.save_msg('Writer was started.', origin='Python-Writer-Test')
while True:
    writer.save([float(datetime.datetime.now().strftime("%S.%f"))], value_type=0x21, origin='Python-Writer-Test')
    sleep(1)