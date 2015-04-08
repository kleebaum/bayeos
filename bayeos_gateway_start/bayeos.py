""" First writer methods """
""" creates a new BayEOS data frame including values given as a list """

import base64
from io import BytesIO
from struct import *
import time
import urllib, urllib2

import pycurl
# try:
#     import urllib.request as urllib2
# except ImportError:
#     import urllib2


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
    for [key, each_value] in values:
        if offsetType == 0x40:  # Data frame with channel indices
            bayeosFrame += pack('b', key)
        if dataType == 0x1:     # float32 4 bytes
            bayeosFrame += pack('f', each_value)
        elif dataType == 0x2:   # int32 4 bytes
            bayeosFrame += pack('i', each_value)   
        elif dataType == 0x3:   # int16 2 bytes
            bayeosFrame += pack('h', each_value)  
        elif dataType == 0x4:   # int8 1 byte
            bayeosFrame += pack('b', each_value)  
        elif dataType == 0x5:   # double 8 bytes
            bayeosFrame += pack('d', each_value)                  
    # print('Data frame created: ', bayeosFrame)
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
    #print('Frame with header (decimal): ', toString(bayeosWriterFrame, header=True))

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

    url = 'http://bayconf.bayceer.uni-bayreuth.de/gateway/frame/saveFlat'
    
    ts = pack('Q', round(unpack('=d', ts)[0] * 1000))
    data = pack("b", 0xc) + ts + data
    postFields = '&sender=' + urllib.quote_plus(name) + '&bayeosframes[]=' + base64.urlsafe_b64encode(data)
    
    username = "admin"
    password = "xbee"

    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
    req = urllib2.Request(url, postFields)
    req.add_header('Accept', 'text/html')
    req.add_header('User-Agent', 'BayEOS-PHP/1.0.8')
    f = opener.open(req)

    if f:
        print "Update OK!"
    else:
        print "Error updating..."
        
    print(f.info())
    
def sendFilePycurl(ts, length, data):
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

    postFields = [('sender', urllib.quote_plus(name)),
      ('password', urllib.quote_plus(pw)),
      ('bayeosframes[]', base64.urlsafe_b64encode(data))
      ]
    curl.setopt(pycurl.HTTPPOST, postFields)
    curl.perform()
    #print('Status ', curl.getinfo(curl.HTTP_CODE))
    #print('Zeit ', curl.getinfo(curl.TOTAL_TIME))
    curl.close()
