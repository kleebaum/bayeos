from struct import *
import pycurl
import time
import urllib.parse
import base64
from io import BytesIO

""" First writer methods """

""" creates a new BayEOS data frame including values given as a list """
def createDataFrame(values, type=0x1, offset=0):
    bayeosFrame = pack('bb', 0x1, type)
    # print('Frame start: ', bayeosFrame)
    offsetType = (0xf0 & type)
    # print('Offset type: ', offsetType)
    dataType = (0x0f & type)
    # print('Data type: ', dataType)    
    if offsetType == 0x0:
        bayeosFrame += pack('b', offset)
        # print('Frame with offset: ', bayeosFrame)        
    for each_value in values:
        bayeosFrame += pack('f', each_value)
    # print('Value frame created: ', bayeosFrame)
    return(bayeosFrame)
    
""" writes a data frame to file according to a time stamp """
def saveDataFrame(values, type=0x1, offset=0, ts=0):
    tmpDir = '/home/anja/tmp/bayeos-device1'
    bayeosFrame = createDataFrame(values, type, offset)
    if not ts:
        ts = time.time()
    bayeosFrameHeaderTs = pack('d', ts)
    # print('Time stamp (binary): ', bayeosFrameHeaderTs)
    bayeosFrameHeaderLength = pack('h', len(bayeosFrame))
    # print('Frame length (decimal): ', len(bayeosFrame))
    # print('Frame length (binary): ', bayeosFrameHeaderLength)
    bayeosWriterFrame = bayeosFrameHeaderTs + bayeosFrameHeaderLength + bayeosFrame
    currentName = tmpDir + '/' + str(time.time()) + '.rd'
    print('File created: ', currentName)
    f = open(currentName, 'wb')    
    f.write(bayeosWriterFrame)
    f.close()
    sendFile(bayeosFrameHeaderTs, bayeosFrameHeaderLength, bayeosFrame)
    # print('Frame with header (binary): ', bayeosWriterFrame)
    print('Frame with header (decimal): ', toString(bayeosWriterFrame, header=True))

""" unpacks the BayEOS data frame """
def toString(bayeosFrame, header=False):
    frameLength = len(bayeosFrame)
    # print('Frame length: ', frameLength)
    if header == True:
        valueLength = (frameLength - 13) / 4
        fmt = '=dhbbb'        
    else:
        valueLength = (frameLength - 3) / 4        
        fmt = '=bbb'
        
    # print('Number of Values: ', valueLength)
    for i in range(0, int(valueLength)):
        fmt += 'f'
    return(unpack(fmt, bayeosFrame))

def sendFile(ts, length, data):
    name = 'PythonTestDevice'
    pw = 'xbee'
    #gatewayVersion = '1.9'

    curl = pycurl.Curl()
    curl.setopt(pycurl.POST, 1)
    
    curl.setopt(pycurl.VERBOSE, 1)
    curl.setopt(pycurl.TIMEOUT, 120)
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.HEADER, 1)
    curl.setopt(pycurl.USERAGENT, 'BayEOS-PHP/1.0.8')
    curl.setopt(pycurl.NOBODY, 1)
    curl.setopt(pycurl.URL, 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat')
    curl.setopt(pycurl.USERPWD, 'admin:xbee')

    ts = pack('Q', round(unpack('=d', ts)[0] * 1000))
    data = pack("b", 0xc) + ts + data

    postFields = [('sender', urllib.parse.quote_plus(name)),
      ('password', urllib.parse.quote_plus(pw)),
      ('bayeosframes[]', base64.urlsafe_b64encode(data))
      ]
    curl.setopt(pycurl.HTTPPOST, postFields)
    curl.perform()
    #print('Status ', curl.getinfo(curl.HTTP_CODE))
    #print('Zeit ', curl.getinfo(curl.TOTAL_TIME))
    curl.close()