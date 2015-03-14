'''creates an example writer'''

import bayeosWriter
from array import array
from time import sleep

def main():
    tmpDir = '/tmp'
    writer = bayeosWriter.BayEOSWriter(tmpDir)
    count = 0
    while True:
        print('adding frame\n')
        writer.saveDataFrame(array(count), 1, 1.0)
        count += 1
        sleep(5)
        