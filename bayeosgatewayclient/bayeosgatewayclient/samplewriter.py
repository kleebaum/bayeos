"""Creates an example writer."""

from time import sleep
from bayeosgatewayclient import BayEOSWriter

PATH = '/tmp/bayeos-device1/'
writer = BayEOSWriter(PATH, 100)

while True:
    print 'adding frame\n'
    writer.save(values=[2.1, 3, 20.5], valueType=0x02, offset=2)
    writer.saveMessage("Dies ist noch eine weitere Nachricht...")
    #writer.saveCommandFrame(1, "command")
    writer.saveErrorMessage("Fehlermeldung")
    sleep(1)
