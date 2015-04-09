import glob
from posix import mkdir, chdir, rename
import os
import time
from struct import *
import string
import urllib, urllib2, base64

from _dbus_bindings import Array
from mutagen.id3._frames import Frame
from requests.api import post
from _sane import FRAME_BLUE

class BayEOS():
    def createDataFrame(self, values, valueType=0x1, offset=0):
        """
        Creates a BayEOS Data Frame.
        @param values: list with [channel index, value] tuples
        @param valueType: defines Offset and Data Types
        @param offset: length of Channel Offset (if Offset Type is 0x0)
        @return Data Frame as a binary string
        """
        frame = pack('bb', 0x1, valueType)          # 0x1 represents data frame 
        offsetType = (0xf0 & valueType)             # first four bits of frame type
        dataType = (0x0f & valueType)               # last four bits of frame type    
        if offsetType == 0x0:                       # data frame with channel offset
                frame += pack('b', offset)          # 1 byte channel offset
        
        for [key, each_value] in values:
            if offsetType == 0x40:                  # data frame with channel indices
                frame += pack('b', key)
            if dataType == 0x1:                     # float32 4 bytes
                frame += pack('f', each_value)
            elif dataType == 0x2:                   # int32 4 bytes
                frame += pack('i', each_value)   
            elif dataType == 0x3:                   # int16 2 bytes
                frame += pack('h', each_value)  
            elif dataType == 0x4:                   # int8 1 byte
                frame += pack('b', each_value)  
            elif dataType == 0x5:                   # double 8 bytes
                frame += pack('d', each_value)  
                    
        return(frame)
            
    def parseFrame(self, frame, ts=False, origin='', rssi=False):
        """
        Parses a binary BayEOS frame into a Python Array.
        @param frame
        @param ts
        @param origin
        @param rssi
        @return array
        """
        if not ts:
            ts = 0
            
    def parseDataFrame(self, frame):
        """
        Parses a BayEOS Data Frame into a PHP Array.
        @param Frame
        @return Array
        """
        pass
    
class BayEOSWriter():
    def __init__(self, path, maxChunk=5000, maxTime=60):
        """ 
        Constructor for a BayEOSWriter instance.
        @param path: path of queue directory
        @param maxChunk: maximum file size when a new file is started
        @param maxTime: maximum time when a new file is started
        """
        self.path = path
        self.maxChunk = maxChunk
        self.maxTime = maxTime
        if not os.path.isdir(self.path):
            #print("try to create new folder")
            os.mkdir(self.path, 0700)
              #  exit("Could not create " + self.path)
                
        chdir(self.path)
        files = glob.glob('*')
        for eachFile in files:
            #print("found file in folder")
            if string.find(eachFile, '.act'):    # Found active file -- unexpected shutdown
                #print("found active file")
                rename(eachFile, eachFile.replace('.act', '.rd'))
        self.startNewFile()
        
    def saveDataFrame(self, values, valueType=0x1, offset=0, ts=0):
        """
        Writes a Data Frame to the buffer.
        @param values: array for values
        @param valueType: defines Offset and Data Types
        @param offset: offset parameter for BayEOS data frames (relevant for some types)
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(BayEOS.createDataFrame(BayEOS(), values, valueType, offset), ts)

    def saveOriginFrame(self, origin, frame, ts=0):
        """
        save origin frame
        @param origin: name to appear in the gateway
        @param frame: must be a valid BayEOS frame
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        origin = origin[0:255]
        self.saveFrame(frame, ts)
    

    def saveRoutedFrameRSSI(self, myId, panId, rssi, frame, ts=0):
        """
        save routed frame RSSI
        @param myId: TX-XBee MyId
        @param panId: XBee PANID
        @param rssi: RSSI
        @param frame: must be a valid BayEOS frame
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(frame, ts)
    
    def saveMessage(self,sting,ts=0):
        """
        save message
        @param sting: message to save
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(sting, ts)
        
    def saveErrorMessage(self, sting, ts=0):
        """
        save error message
        @param sting: message to save
        @param ts: Unix epoch time stamp, if zero system time is used
        """
        self.saveFrame(sting, ts)
        

    def saveFrame(self, frame, ts=0):
        """Save Timestamp Frame to file. This is a base function.
        @param frame: must be a valid BayEOS Frame
        @param ts: Unix epoch time stamp, if zero system time is used 
        """
        if not ts:
            ts = time.time()
        self.fp.write(pack('d', ts) + pack('h', len(frame)) + frame)
        if self.fp.tell() > self.maxChunk or time.time() - self.currentTs > self.maxTime:
            self.fp.close()
            rename(self.currentName + '.act', self.currentName + '.rd')
            self.startNewFile()
    
    def startNewFile(self):
        """ Opens a new file with ending .act and determines current file name. """ 
        self.currentTs = time.time()
        [sec, usec] = string.split(str(self.currentTs), '.')
        self.currentName = sec + '-' + usec
        self.fp = open(self.currentName + '.act', 'wb')
        
class BayEOSSender():
    def __init__(self, path, name, url, pw, user='import', absoluteTime=True, rm=True, gatewayVersion='1.9'):
        """
        Constructor for BayEOSSender instance.
        @param path: path where BayEOSWriter puts files
        @param name: sender name
        @param url: gateway url e.g. http://<gateway>/gateway/frame/saveFlat
        @param pw: password on gateway
        @param user: user on gateway
        @param absoluteTime: if set to false, relative time is used (delay)
        @param rm: if set to false files are kept as .bak file in the BayEOSWriter directory
        @param gatewayVersion: gateway version
        """
#         try:
#             urllib2.urlopen(url)
#         except:
#             exit("URL " + url + " is not valid.\n")
        if not pw:
            exit("No gateway password was found.\n")
        self.path = path
        self.name = name
        self.url = url
        self.pw = pw
        self.user = user
        self.absoluteTime = absoluteTime
        self.rm = rm
        self.gatewayVersion = gatewayVersion
        self.lengthOfDouble = len(pack('d', time.time()))
        self.lengthOfShort = len(pack('h', 1))
    
    def send(self):
        """
        Keeps sending until all files are sent or an error occurs.
        @return number of post requests as an integer
        """
        countFrames = 0
        while(post == self.sendFile()):
            countFrames += post
        return(countFrames)
    
    def sendFile(self):
        """
        Reads one file from queue and tries to send it to the gateway.
        On success file is deleted or renamed to *.bak ending.
        Always the oldest file is used.
        """
        chdir(self.path)
        files = glob.glob('*.rd')
        if len(files) == 0:
            return 0
        fp = open(files[0], 'rb') # opens oldest file
        data = '&sender=' + urllib.quote_plus(self.name)
        
        count = 0
        print(fp)
        ts = fp.read(self.lengthOfDouble)
        if ts:
            ts = unpack('=d', ts)[0]
            frameLength = unpack('=h', fp.read(self.lengthOfShort))[0]
            frame = fp.read(frameLength)
            if len(frame) != 0:
                ++count
                timestampFrame = pack('b', 0xc) + pack('Q', round(ts * 1000)) + frame
                data += '&bayeosframes[]=' + base64.urlsafe_b64encode(timestampFrame)
        fp.close()
        self.post(data)
        if self.rm:
            os.remove(files[0])
        #return(count)
            
        
    def post(self, data):
        """
        Posts frames to gateway.
        @param postData
        @return success
        """
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.url, self.user, self.pw)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(self.url, data)
        req.add_header('Accept', 'text/html')
        req.add_header('User-Agent', 'BayEOS-PHP/1.0.8')
        post = opener.open(req)        

class BayEOSGatewayClient():
    """
    create an instance of bayeosGatewayClient
    @param names: name array e.g. 'Fifo.0', 'Fifo.1'..., used for storage directory e.g. /tmp/Fifo.0
    @param options
    """
    def __init__(self, names, options, defaults):
        pass
    
    """
    helper function to get an option value
    @param key
    @param default
    @return string: value of the specified option key
    """
    def getOption(self, key, default=''):
        pass
    
    """
    runs the BayEOSGatewayClient
    forks one BayEOSWrite and one BayEOSSender per name
    """
    def run(self):
        pass
    
    """
    method called by run()
    can be overwritten by implementation
    """
    def initWriter(self):
        pass
    
    """
    method called by run()
    must be overwritten by implementation
    """
    def readData(self):
        exit("no readData() found!\n")
        return(False)
    
    """
    method called by run()
    can be overwritten by implementation (e.g. to store routed frames)
    """    
    def saveData(self, data):
        pass  


     